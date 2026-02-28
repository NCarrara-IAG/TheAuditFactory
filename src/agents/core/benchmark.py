"""Agent Benchmark — scoring maturité et comparaison aux standards industrie."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict

from src.agents.base import BaseAgent
from src.agents.core.prompts import BENCHMARK_PROMPT
from src.orchestrator.router import get_maturity_dimensions
from src.schemas.models import AgentOutput

logger = logging.getLogger(__name__)


class BenchmarkAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="benchmark",
            agent_name="Benchmark",
            system_prompt=BENCHMARK_PROMPT,
        )

    def run(self, state: Dict[str, Any]) -> AgentOutput:
        started = datetime.now(timezone.utc)
        logger.info(f"[{self.agent_id}] Starting analysis")

        dimensions = get_maturity_dimensions(state["audit_type"])
        prompt = self.system_prompt.format(
            maturity_dimensions="\n".join(f"- {d}" for d in dimensions)
        )

        ctx = state.get("client_context", {})
        user_message = (
            f"Contexte client :\n"
            f"- Entreprise : {ctx.get('name', 'N/A')}\n"
            f"- Industrie : {ctx.get('industry', 'N/A')}\n"
            f"- Documents : {ctx.get('docs_provided', [])}\n\n"
            f"Score chaque dimension de maturité de 1 à 5."
        )

        raw = self.invoke_llm(user_message)
        output = self.parse_output(raw)
        output.metadata["timeline"] = self.build_timeline_entry(started)
        return output
