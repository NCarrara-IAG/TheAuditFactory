"""Agent Risk & Compliance — risques cyber, RGPD, dépendances critiques."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict

from src.agents.base import BaseAgent
from src.agents.core.prompts import RISK_COMPLIANCE_PROMPT
from src.schemas.models import AgentOutput

logger = logging.getLogger(__name__)


class RiskComplianceAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="risk_compliance",
            agent_name="Risk & Compliance",
            system_prompt=RISK_COMPLIANCE_PROMPT,
        )

    def run(self, state: Dict[str, Any]) -> AgentOutput:
        started = datetime.now(timezone.utc)
        logger.info(f"[{self.agent_id}] Starting analysis")

        ctx = state.get("client_context", {})
        user_message = (
            f"Contexte client :\n"
            f"- Entreprise : {ctx.get('name', 'N/A')}\n"
            f"- Industrie : {ctx.get('industry', 'N/A')}\n"
            f"- Documents : {ctx.get('docs_provided', [])}\n\n"
            f"Identifie tous les risques et enjeux de conformité."
        )

        raw = self.invoke_llm(user_message)
        output = self.parse_output(raw)
        output.metadata["timeline"] = self.build_timeline_entry(started)
        return output
