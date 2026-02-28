"""Agent Prioritization Engine — scoring, quick wins, roadmap."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict

from src.agents.base import BaseAgent
from src.agents.core.prompts import PRIORITIZATION_ENGINE_PROMPT
from src.schemas.models import AgentOutput

logger = logging.getLogger(__name__)


class PrioritizationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="prioritization",
            agent_name="Prioritization Engine",
            system_prompt=PRIORITIZATION_ENGINE_PROMPT,
        )

    def run(self, state: Dict[str, Any]) -> AgentOutput:
        started = datetime.now(timezone.utc)
        logger.info(f"[{self.agent_id}] Starting prioritization")

        user_message = (
            f"Recommandations à prioriser :\n{state.get('recommendations', [])}\n\n"
            f"Risques identifiés :\n{state.get('risks', [])}\n\n"
            f"Findings :\n{state.get('findings', [])}\n\n"
            f"Score et classe chaque recommandation. "
            f"Identifie les quick wins et construis la roadmap 3/6/12 mois."
        )

        raw = self.invoke_llm(user_message)
        output = self.parse_output(raw)
        output.metadata["timeline"] = self.build_timeline_entry(started)
        return output
