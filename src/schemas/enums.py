"""Enumerations shared across the entire Audit Factory."""

from enum import Enum


class AuditType(str, Enum):
    # Niveau A — Audits stratégiques (COMEX level)
    STRATEGIC_GLOBAL = "strategic_global"
    STRATEGIC_PRODUCT = "strategic_product"
    STRATEGIC_COST = "strategic_cost"
    STRATEGIC_DATA_IA = "strategic_data_ia"
    STRATEGIC_SCALE = "strategic_scale"
    # Niveau B — Audits opérationnels
    IA_READINESS = "ia_readiness"
    SMART_FACTORY = "smart_factory"
    IT_ARCHITECTURE = "it_architecture"
    PRODUCT_DELIVERY = "product_delivery"


AUDIT_TYPE_LABELS: dict[AuditType, str] = {
    AuditType.STRATEGIC_GLOBAL: "Audit stratégique global de situation",
    AuditType.STRATEGIC_PRODUCT: "Audit stratégique Produit & Innovation",
    AuditType.STRATEGIC_COST: "Audit stratégique Rationalisation & coûts",
    AuditType.STRATEGIC_DATA_IA: "Audit stratégique Maturité Data / IA / IoT",
    AuditType.STRATEGIC_SCALE: "Audit stratégique Passage à l'échelle",
    AuditType.IA_READINESS: "Audit IA Readiness",
    AuditType.SMART_FACTORY: "Audit Smart Factory / Industrie 4.0",
    AuditType.IT_ARCHITECTURE: "Audit IT & Architecture",
    AuditType.PRODUCT_DELIVERY: "Audit Product & Delivery",
}


class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Probability(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Effort(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Impact(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Timeframe(str, Enum):
    QUICK_WIN = "QUICK_WIN"
    THREE_MONTHS = "3_MONTHS"
    SIX_MONTHS = "6_MONTHS"
    TWELVE_MONTHS = "12_MONTHS"


class MaturityLevel(int, Enum):
    INITIAL = 1
    MANAGED = 2
    DEFINED = 3
    MEASURED = 4
    OPTIMIZED = 5


class AuditPhase(str, Enum):
    INIT = "init"
    INTAKE = "intake"
    CORE_ANALYSIS = "core_analysis"
    PLUGIN_ANALYSIS = "plugin_analysis"
    CONSOLIDATION = "consolidation"
    ROI_PRIORITY = "roi_priority"
    VALIDATION = "validation"
    REPORTING = "reporting"
    COMPLETE = "complete"


class ScenarioType(str, Enum):
    CONSERVATIVE = "conservative"
    TARGET = "target"
    AMBITIOUS = "ambitious"
