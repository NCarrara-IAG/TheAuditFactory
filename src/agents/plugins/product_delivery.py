"""Plugin Agent — Product & Delivery Evaluator."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict

from src.agents.base import BaseAgent
from src.agents.core.prompts import PLUGIN_AGENT_PROMPT_TEMPLATE
from src.schemas.models import AgentOutput

logger = logging.getLogger(__name__)

PRODUCT_DELIVERY_PROMPT = PLUGIN_AGENT_PROMPT_TEMPLATE.format(
    plugin_name="Product & Delivery Evaluator",
    agent_id="product_delivery",
    id_prefix="PD",
    expertise_description=(
        "Expert en product management, méthodologies agiles, delivery pipeline, "
        "organisation produit et time-to-market."
    ),
    mission=(
        "Évaluer la maturité produit & delivery du client :\n"
        "1. **Time-to-market** : cycle idée→production, lead time, cycle time\n"
        "2. **Organisation produit** : PM, PO, discovery/delivery separation\n"
        "3. **Méthodologie** : agile maturity, rituels, continuous improvement\n"
        "4. **Cross-team collaboration** : frictions, dépendances inter-équipes\n"
        "5. **Delivery pipeline** : release frequency, rollback capability, feature flags"
    ),
    analysis_dimensions=(
        "- Time-to-Market (lead time, cycle time, bottlenecks)\n"
        "- Product Organization (PM/PO structure, empowerment)\n"
        "- Methodology Maturity (agile, rituels, kaizen)\n"
        "- Cross-team Collaboration (deps, frictions)\n"
        "- Delivery Pipeline (CI/CD, releases, feature flags)"
    ),
)


class ProductDeliveryPlugin(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="product_delivery",
            agent_name="Product & Delivery Evaluator",
            system_prompt=PRODUCT_DELIVERY_PROMPT,
        )

    def run(self, state: Dict[str, Any]) -> AgentOutput:
        started = datetime.now(timezone.utc)
        logger.info(f"[{self.agent_id}] Starting Product & Delivery evaluation")

        ctx = state.get("client_context", {})
        user_message = (
            f"Contexte client : {ctx.get('name', 'N/A')} — {ctx.get('industry', 'N/A')}\n"
            f"Documents : {ctx.get('docs_provided', [])}\n\n"
            f"Évalue la maturité produit, le time-to-market et la delivery."
        )

        raw = self.invoke_llm(user_message)
        output = self.parse_output(raw)
        output.metadata["timeline"] = self.build_timeline_entry(started)
        return output
