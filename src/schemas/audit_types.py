"""Catalogue des 9 types d'audits avec leur configuration d'agents.

Chaque type d'audit définit :
- les dimensions de maturité à scorer
- les agents plugins spécialisés à activer
- le descriptif métier
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .enums import AuditType


@dataclass(frozen=True)
class AuditTypeConfig:
    audit_type: AuditType
    label: str
    level: str  # "A" (stratégique) ou "B" (opérationnel)
    objective: str
    maturity_dimensions: List[str]
    plugin_agents: List[str]
    deliverable_extras: List[str] = field(default_factory=list)


AUDIT_CATALOGUE: dict[AuditType, AuditTypeConfig] = {
    # -----------------------------------------------------------------------
    # NIVEAU A — Audits stratégiques (COMEX level)
    # -----------------------------------------------------------------------
    AuditType.STRATEGIC_GLOBAL: AuditTypeConfig(
        audit_type=AuditType.STRATEGIC_GLOBAL,
        label="Audit stratégique global de situation",
        level="A",
        objective="Vision claire partagée avant décision structurante",
        maturity_dimensions=[
            "strategy_alignment", "org_maturity", "tech_foundation",
            "data_governance", "product_capability", "operational_excellence",
        ],
        plugin_agents=["strategic_global_analyst"],
    ),
    AuditType.STRATEGIC_PRODUCT: AuditTypeConfig(
        audit_type=AuditType.STRATEGIC_PRODUCT,
        label="Audit stratégique Produit & Innovation",
        level="A",
        objective="Capacité à innover utilement et transformer en produits à impact",
        maturity_dimensions=[
            "discovery_practice", "delivery_practice", "product_org",
            "innovation_pipeline", "business_tech_alignment",
        ],
        plugin_agents=["product_innovation_analyst", "time_to_market_analyzer"],
    ),
    AuditType.STRATEGIC_COST: AuditTypeConfig(
        audit_type=AuditType.STRATEGIC_COST,
        label="Audit stratégique Rationalisation & coûts",
        level="A",
        objective="Identifier leviers d'économies mesurables",
        maturity_dimensions=[
            "cost_visibility", "stack_rationalization", "vendor_management",
            "license_optimization", "operational_efficiency",
        ],
        plugin_agents=["stack_redundancy_detector", "cloud_cost_analyzer"],
    ),
    AuditType.STRATEGIC_DATA_IA: AuditTypeConfig(
        audit_type=AuditType.STRATEGIC_DATA_IA,
        label="Audit stratégique Maturité Data / IA / IoT",
        level="A",
        objective="Mesurer écart ambition vs réalité opérationnelle",
        maturity_dimensions=[
            "data_governance", "data_quality", "ai_readiness",
            "iot_integration", "mlops_maturity", "ai_governance",
        ],
        plugin_agents=["ia_readiness", "iot_readiness_evaluator"],
    ),
    AuditType.STRATEGIC_SCALE: AuditTypeConfig(
        audit_type=AuditType.STRATEGIC_SCALE,
        label="Audit stratégique Passage à l'échelle",
        level="A",
        objective="Sécuriser industrialisation et éviter échecs coûteux",
        maturity_dimensions=[
            "poc_success_rate", "industrialization_readiness",
            "infra_scalability", "team_scaling", "process_automation",
        ],
        plugin_agents=["poc_failure_analyzer", "scale_readiness_evaluator"],
    ),
    # -----------------------------------------------------------------------
    # NIVEAU B — Audits opérationnels
    # -----------------------------------------------------------------------
    AuditType.IA_READINESS: AuditTypeConfig(
        audit_type=AuditType.IA_READINESS,
        label="Audit IA Readiness",
        level="B",
        objective="Maturité data, cas d'usage IA, ROI potentiel, gouvernance IA",
        maturity_dimensions=[
            "data_governance", "data_quality", "ai_use_cases",
            "ai_roi_potential", "ai_governance", "mlops_readiness",
        ],
        plugin_agents=["ia_readiness", "mlops_readiness_agent"],
    ),
    AuditType.SMART_FACTORY: AuditTypeConfig(
        audit_type=AuditType.SMART_FACTORY,
        label="Audit Smart Factory / Industrie 4.0",
        level="B",
        objective="IoT readiness, flux data machines, maintenance prédictive, archi SI industrielle",
        maturity_dimensions=[
            "iot_connectivity", "machine_data_flow", "predictive_maintenance",
            "ot_it_integration", "industrial_si_architecture",
        ],
        plugin_agents=["smart_factory_evaluator", "ot_it_integration_evaluator"],
    ),
    AuditType.IT_ARCHITECTURE: AuditTypeConfig(
        audit_type=AuditType.IT_ARCHITECTURE,
        label="Audit IT & Architecture",
        level="B",
        objective="Dette technique, sécurité, scalabilité, coûts cloud",
        maturity_dimensions=[
            "tech_debt", "security_posture", "scalability",
            "cloud_cost_efficiency", "devops_maturity", "observability",
        ],
        plugin_agents=["it_architecture_evaluator", "cloud_cost_analyzer"],
    ),
    AuditType.PRODUCT_DELIVERY: AuditTypeConfig(
        audit_type=AuditType.PRODUCT_DELIVERY,
        label="Audit Product & Delivery",
        level="B",
        objective="Time-to-market, organisation produit, méthodologie, frictions inter-équipes",
        maturity_dimensions=[
            "time_to_market", "product_org", "methodology_maturity",
            "cross_team_collaboration", "delivery_pipeline",
        ],
        plugin_agents=["product_delivery_evaluator", "time_to_market_analyzer"],
    ),
}


def get_audit_config(audit_type: AuditType) -> AuditTypeConfig:
    return AUDIT_CATALOGUE[audit_type]
