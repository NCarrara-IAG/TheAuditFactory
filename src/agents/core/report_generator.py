"""Agent Report Generator — executive summary, slides, roadmap."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict

from src.agents.base import BaseAgent
from src.agents.core.prompts import REPORT_GENERATOR_PROMPT
from src.schemas.models import AgentOutput

logger = logging.getLogger(__name__)


class ReportGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="report_generator",
            agent_name="Report Generator",
            system_prompt=REPORT_GENERATOR_PROMPT,
        )

    def run(self, state: Dict[str, Any]) -> AgentOutput:
        started = datetime.now(timezone.utc)
        logger.info(f"[{self.agent_id}] Generating deliverables")

        ctx = state.get("client_context", {})
        user_message = (
            f"Contexte client : {ctx.get('name', 'N/A')} — {ctx.get('industry', 'N/A')}\n"
            f"Type d'audit : {state.get('audit_type', 'N/A')}\n\n"
            f"Findings consolidés ({len(state.get('findings', []))}) :\n"
            f"{state.get('findings', [])}\n\n"
            f"Risques ({len(state.get('risks', []))}) :\n"
            f"{state.get('risks', [])}\n\n"
            f"Recommandations ({len(state.get('recommendations', []))}) :\n"
            f"{state.get('recommendations', [])}\n\n"
            f"Scores maturité : {state.get('maturity_scores', {})}\n"
            f"ROI Model : {state.get('roi_model', {})}\n"
            f"Quick wins : {state.get('quick_wins', [])}\n"
            f"Roadmap : {state.get('roadmap', [])}\n"
            f"Scénarios : {state.get('scenarios', [])}\n\n"
            f"Génère l'Executive Summary, les slides et la roadmap structurée."
        )

        raw = self.invoke_llm(user_message)
        output = self.parse_output(raw)
        output.metadata["timeline"] = self.build_timeline_entry(started)
        return output
