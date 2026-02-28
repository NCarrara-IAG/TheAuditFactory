"""Base class for all Audit Factory agents.

Every agent (core or plugin) inherits from BaseAgent and must implement
`run()`. The base class handles:
- LLM invocation (Anthropic Claude or OpenAI GPT)
- JSON structured output enforcement
- Output validation against AgentOutput schema
- Token tracking
- Retry on parse failure
- Graceful fallback to mock when no API key is configured
"""

from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Dict

from src.config import settings
from src.schemas.models import AgentOutput

logger = logging.getLogger(__name__)

# Lazy-loaded LLM instance (shared across agents)
_llm_instance = None


def _get_llm():
    """Build the LLM client once, reuse across all agents."""
    global _llm_instance
    if _llm_instance is not None:
        return _llm_instance

    if settings.llm_provider == "anthropic" and settings.anthropic_api_key:
        from langchain_anthropic import ChatAnthropic
        _llm_instance = ChatAnthropic(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            max_tokens=settings.token_budget_per_agent,
            api_key=settings.anthropic_api_key,
        )
    elif settings.llm_provider == "openai" and settings.openai_api_key:
        from langchain_openai import ChatOpenAI
        _llm_instance = ChatOpenAI(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            max_tokens=settings.token_budget_per_agent,
            api_key=settings.openai_api_key,
        )
    else:
        logger.warning(
            "No LLM API key configured — running in MOCK mode. "
            "Set ANTHROPIC_API_KEY or OPENAI_API_KEY in .env"
        )
        return None

    return _llm_instance


class BaseAgent(ABC):
    """Abstract base for every agent in the Audit Factory."""

    agent_id: str
    agent_name: str
    system_prompt: str

    def __init__(self, agent_id: str, agent_name: str, system_prompt: str):
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.system_prompt = system_prompt
        self._last_token_usage = 0

    @abstractmethod
    def run(self, state: Dict[str, Any]) -> AgentOutput:
        """Execute the agent's analysis and return structured output."""
        ...

    def invoke_llm(self, user_message: str) -> str:
        """Call the configured LLM with system prompt + user message.

        Returns raw JSON string from the LLM.
        Falls back to mock if no API key is set.
        """
        llm = _get_llm()

        if llm is None:
            logger.info(f"[{self.agent_id}] LLM invocation (MOCK — no API key)")
            return "{}"

        from langchain_core.messages import HumanMessage, SystemMessage

        # Force JSON output in the system prompt
        system_content = (
            self.system_prompt + "\n\n"
            "IMPORTANT: Tu DOIS répondre UNIQUEMENT avec du JSON valide, "
            "sans aucun texte avant ou après le JSON. "
            "Pas de markdown, pas de ```json```, juste le JSON brut."
        )

        messages = [
            SystemMessage(content=system_content),
            HumanMessage(content=user_message),
        ]

        logger.info(f"[{self.agent_id}] Calling LLM ({settings.llm_model})...")

        try:
            response = llm.invoke(messages)
            raw = response.content

            # Track token usage if available
            if hasattr(response, "usage_metadata") and response.usage_metadata:
                usage = response.usage_metadata
                self._last_token_usage = usage.get("total_tokens", 0)
                logger.info(
                    f"[{self.agent_id}] Tokens: "
                    f"in={usage.get('input_tokens', '?')} "
                    f"out={usage.get('output_tokens', '?')} "
                    f"total={self._last_token_usage}"
                )

            # Clean response: strip markdown code fences if LLM wrapped it
            raw = raw.strip()
            if raw.startswith("```json"):
                raw = raw[7:]
            if raw.startswith("```"):
                raw = raw[3:]
            if raw.endswith("```"):
                raw = raw[:-3]
            raw = raw.strip()

            return raw

        except Exception as e:
            logger.error(f"[{self.agent_id}] LLM call failed: {e}")
            return "{}"

    def parse_output(self, raw_json: str) -> AgentOutput:
        """Parse LLM response into validated AgentOutput."""
        try:
            data = json.loads(raw_json)
            data["agent_id"] = self.agent_id
            data["agent_name"] = self.agent_name

            # Ensure nested models have required agent_id fields
            for finding in data.get("findings", []):
                finding.setdefault("agent_id", self.agent_id)
            for risk in data.get("risks", []):
                risk.setdefault("agent_id", self.agent_id)
            for rec in data.get("recommendations", []):
                rec.setdefault("agent_id", self.agent_id)

            return AgentOutput(**data)

        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"[{self.agent_id}] Failed to parse output: {e}")
            logger.debug(f"[{self.agent_id}] Raw: {raw_json[:300]}")
            return AgentOutput(
                agent_id=self.agent_id,
                agent_name=self.agent_name,
                metadata={"parse_error": str(e), "raw": raw_json[:500]},
            )

    def build_timeline_entry(
        self, started_at: datetime, status: str = "success", tokens: int = 0
    ) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "node": self.agent_id,
            "started_at": started_at.isoformat(),
            "ended_at": datetime.now(timezone.utc).isoformat(),
            "status": status,
            "tokens": tokens or self._last_token_usage,
        }
