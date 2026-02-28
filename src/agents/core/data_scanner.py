"""Agent Data Scanner — cartographie technique et extraction d'entités."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict

from src.agents.base import BaseAgent
from src.agents.core.prompts import DATA_SCANNER_PROMPT
from src.schemas.models import AgentOutput

logger = logging.getLogger(__name__)


class DataScannerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="data_scanner",
            agent_name="Data Scanner",
            system_prompt=DATA_SCANNER_PROMPT,
        )

    def run(self, state: Dict[str, Any]) -> AgentOutput:
        started = datetime.now(timezone.utc)
        logger.info(f"[{self.agent_id}] Starting analysis")

        # Build context from state
        docs = state.get("client_context", {}).get("docs_provided", [])
        sources_index = state.get("sources_index", {})

        user_message = (
            f"Voici le contexte client :\n"
            f"- Entreprise : {state['client_context'].get('name', 'N/A')}\n"
            f"- Industrie : {state['client_context'].get('industry', 'N/A')}\n"
            f"- Documents fournis : {docs}\n"
            f"- Index des sources : {sources_index}\n\n"
            f"Analyse ces documents et produis ta cartographie technique."
        )

        raw = self.invoke_llm(user_message)
        output = self.parse_output(raw)
        output.metadata["timeline"] = self.build_timeline_entry(started)
        return output
