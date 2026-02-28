"""Agent Process Mapper — reconstitution des flux métier et frictions."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict

from src.agents.base import BaseAgent
from src.agents.core.prompts import PROCESS_MAPPER_PROMPT
from src.schemas.models import AgentOutput

logger = logging.getLogger(__name__)


class ProcessMapperAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="process_mapper",
            agent_name="Process Mapper",
            system_prompt=PROCESS_MAPPER_PROMPT,
        )

    def run(self, state: Dict[str, Any]) -> AgentOutput:
        started = datetime.now(timezone.utc)
        logger.info(f"[{self.agent_id}] Starting analysis")

        ctx = state.get("client_context", {})
        user_message = (
            f"Contexte client :\n"
            f"- Entreprise : {ctx.get('name', 'N/A')}\n"
            f"- Industrie : {ctx.get('industry', 'N/A')}\n"
            f"- Objectifs : {ctx.get('objectives', 'N/A')}\n"
            f"- Documents : {ctx.get('docs_provided', [])}\n\n"
            f"Reconstitue les flux métier et identifie les frictions."
        )

        raw = self.invoke_llm(user_message)
        output = self.parse_output(raw)
        output.metadata["timeline"] = self.build_timeline_entry(started)
        return output
