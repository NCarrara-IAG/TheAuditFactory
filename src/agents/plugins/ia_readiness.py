"""Plugin Agent — IA Readiness Evaluator.

Spécialisé dans l'évaluation de la maturité IA d'une organisation :
gouvernance data, cas d'usage IA, ROI potentiel, MLOps readiness.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict

from src.agents.base import BaseAgent
from src.agents.core.prompts import PLUGIN_AGENT_PROMPT_TEMPLATE
from src.schemas.models import AgentOutput

logger = logging.getLogger(__name__)

IA_READINESS_PROMPT = PLUGIN_AGENT_PROMPT_TEMPLATE.format(
    plugin_name="IA Readiness Evaluator",
    agent_id="ia_readiness",
    id_prefix="IAR",
    expertise_description=(
        "Expert en intelligence artificielle appliquée, data science, MLOps et "
        "gouvernance IA. Tu évalues la capacité d'une organisation à tirer parti "
        "de l'IA de manière responsable et rentable."
    ),
    mission=(
        "Évaluer la maturité IA du client sur 6 axes :\n"
        "1. **Gouvernance data** : qualité, catalogage, lineage, ownership\n"
        "2. **Qualité des données** : complétude, fraîcheur, accessibilité\n"
        "3. **Cas d'usage IA** : identifier les 3-5 use cases à plus fort ROI\n"
        "4. **ROI potentiel IA** : estimation des gains par use case\n"
        "5. **Gouvernance IA** : éthique, biais, explicabilité, conformité AI Act\n"
        "6. **MLOps readiness** : pipeline ML, monitoring, déploiement, A/B testing"
    ),
    analysis_dimensions=(
        "- Data Governance (ownership, catalogue, lineage)\n"
        "- Data Quality (complétude, fraîcheur, format)\n"
        "- AI Use Cases (identification, priorisation, faisabilité)\n"
        "- AI ROI Potential (gains estimés par use case)\n"
        "- AI Governance (éthique, biais, explicabilité, AI Act)\n"
        "- MLOps Readiness (CI/CD ML, monitoring, feature store)"
    ),
)


class IAReadinessAgent:
    def __init__(self):
        self.plugin_name = "IA Readiness Evaluator"
        self.directives = "Maturité data, cas d'usage IA, ROI potentiel, gouvernance IA"
        # We can reuse the shared LLM if passed, but for now we'll initialize
        self.llm = ChatAnthropic(model="claude-3-5-sonnet-latest", temperature=0)

    def analyze(self, context: dict):
        print(f"[{self.plugin_name}] Analyzing via Claude...")
        
        # Use structured output for Findings
        # Note: In a real complex agent, we might want a list of Findings.
        # For this MVP, we'll ask for one prominent finding.
        structured_llm = self.llm.with_structured_output(Finding)
        
        prompt = PLUGIN_PATTERN_PROMPT.format(
            plugin_name=self.plugin_name,
            directives=self.directives
        )
        
        try:
            finding = structured_llm.invoke([
                ("system", prompt),
                ("human", f"Context: {context}")
            ])
            return {"findings": [finding]}
        except Exception as e:
            print(f"Error in {self.plugin_name}: {e}")
            return {"findings": []}
