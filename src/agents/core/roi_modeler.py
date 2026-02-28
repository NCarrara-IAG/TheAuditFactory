"""Agent ROI Modeler — modélisation financière, 3 scénarios, payback."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict

from src.agents.base import BaseAgent
from src.agents.core.prompts import ROI_MODELER_PROMPT
from src.schemas.models import AgentOutput

logger = logging.getLogger(__name__)


class ROIModelerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="roi_modeler",
            agent_name="ROI Modeler",
            system_prompt=ROI_MODELER_PROMPT,
        )

    def run(self, state: Dict[str, Any]) -> AgentOutput:
        started = datetime.now(timezone.utc)
        logger.info(f"[{self.agent_id}] Starting ROI modeling")

        ctx = state.get("client_context", {})
        user_message = (
            f"Contexte client :\n"
            f"- Entreprise : {ctx.get('name', 'N/A')}\n"
            f"- Industrie : {ctx.get('industry', 'N/A')}\n\n"
            f"Recommandations consolidées :\n{state.get('recommendations', [])}\n\n"
            f"Risques consolidés :\n{state.get('risks', [])}\n\n"
            f"Produis 3 scénarios ROI (conservateur / target / ambitieux)."
        )

        raw = self.invoke_llm(user_message)
        output = self.parse_output(raw)
        output.metadata["timeline"] = self.build_timeline_entry(started)
        return output
