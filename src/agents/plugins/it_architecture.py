"""Plugin Agent — IT & Architecture Evaluator."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict

from src.agents.base import BaseAgent
from src.agents.core.prompts import PLUGIN_AGENT_PROMPT_TEMPLATE
from src.schemas.models import AgentOutput

logger = logging.getLogger(__name__)

IT_ARCH_PROMPT = PLUGIN_AGENT_PROMPT_TEMPLATE.format(
    plugin_name="IT Architecture Evaluator",
    agent_id="it_architecture",
    id_prefix="ITA",
    expertise_description=(
        "Expert en architecture technique, dette technique, sécurité SI, "
        "scalabilité, cloud economics et DevOps."
    ),
    mission=(
        "Évaluer l'architecture IT du client :\n"
        "1. **Dette technique** : code legacy, frameworks obsolètes, couplage\n"
        "2. **Sécurité** : posture, vulnérabilités, IAM, chiffrement\n"
        "3. **Scalabilité** : capacité à absorber la croissance\n"
        "4. **Cloud cost efficiency** : FinOps, reserved instances, right-sizing\n"
        "5. **DevOps maturity** : CI/CD, IaC, observabilité, SRE\n"
        "6. **Stack rationalization** : redondances, licences sous-utilisées"
    ),
    analysis_dimensions=(
        "- Tech Debt (legacy, obsolescence, couplage)\n"
        "- Security Posture (vulnérabilités, IAM, chiffrement)\n"
        "- Scalability (infra, horizontal/vertical)\n"
        "- Cloud Cost Efficiency (FinOps, right-sizing)\n"
        "- DevOps Maturity (CI/CD, IaC, observability)\n"
        "- Stack Rationalization (redondances, licences)"
    ),
)


class ITArchitecturePlugin(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="it_architecture",
            agent_name="IT Architecture Evaluator",
            system_prompt=IT_ARCH_PROMPT,
        )

    def run(self, state: Dict[str, Any]) -> AgentOutput:
        started = datetime.now(timezone.utc)
        logger.info(f"[{self.agent_id}] Starting IT Architecture evaluation")

        ctx = state.get("client_context", {})
        user_message = (
            f"Contexte client : {ctx.get('name', 'N/A')} — {ctx.get('industry', 'N/A')}\n"
            f"Documents : {ctx.get('docs_provided', [])}\n\n"
            f"Évalue l'architecture IT, la dette technique et les coûts cloud."
        )

        raw = self.invoke_llm(user_message)
        output = self.parse_output(raw)
        output.metadata["timeline"] = self.build_timeline_entry(started)
        return output
