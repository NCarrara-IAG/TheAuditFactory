"""Plugin Agent — Smart Factory / Industrie 4.0 Evaluator."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict

from src.agents.base import BaseAgent
from src.agents.core.prompts import PLUGIN_AGENT_PROMPT_TEMPLATE
from src.schemas.models import AgentOutput

logger = logging.getLogger(__name__)

SMART_FACTORY_PROMPT = PLUGIN_AGENT_PROMPT_TEMPLATE.format(
    plugin_name="Smart Factory Evaluator",
    agent_id="smart_factory",
    id_prefix="SF",
    expertise_description=(
        "Expert en Industrie 4.0, IoT industriel, OT/IT convergence, "
        "maintenance prédictive et architectures SI industrielles."
    ),
    mission=(
        "Évaluer la maturité Industrie 4.0 du client :\n"
        "1. **IoT connectivity** : capteurs, protocoles, edge computing\n"
        "2. **Machine data flow** : collecte, transmission, stockage temps réel\n"
        "3. **Maintenance prédictive** : modèles, alertes, ROI maintenance\n"
        "4. **OT/IT integration** : convergence réseaux, sécurité industrielle\n"
        "5. **Architecture SI industrielle** : MES, SCADA, ERP integration"
    ),
    analysis_dimensions=(
        "- IoT Connectivity (capteurs, protocoles, edge)\n"
        "- Machine Data Flow (collecte, stockage, real-time)\n"
        "- Predictive Maintenance (modèles, alertes)\n"
        "- OT/IT Integration (convergence, sécurité)\n"
        "- Industrial SI Architecture (MES, SCADA, ERP)"
    ),
)


class SmartFactoryPlugin(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="smart_factory",
            agent_name="Smart Factory Evaluator",
            system_prompt=SMART_FACTORY_PROMPT,
        )

    def run(self, state: Dict[str, Any]) -> AgentOutput:
        started = datetime.now(timezone.utc)
        logger.info(f"[{self.agent_id}] Starting Smart Factory evaluation")

        ctx = state.get("client_context", {})
        user_message = (
            f"Contexte client : {ctx.get('name', 'N/A')} — {ctx.get('industry', 'N/A')}\n"
            f"Documents : {ctx.get('docs_provided', [])}\n\n"
            f"Évalue la maturité Industrie 4.0."
        )

        raw = self.invoke_llm(user_message)
        output = self.parse_output(raw)
        output.metadata["timeline"] = self.build_timeline_entry(started)
        return output
