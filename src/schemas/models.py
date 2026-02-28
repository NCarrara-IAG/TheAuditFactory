"""Core domain models for the Audit Factory.

Every agent output, finding, risk, and recommendation flows through these
Pydantic models to guarantee JSON-schema validation and traceability.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .enums import (
    Effort,
    Impact,
    MaturityLevel,
    Probability,
    ScenarioType,
    Severity,
    Timeframe,
)


# ---------------------------------------------------------------------------
# Traçabilité
# ---------------------------------------------------------------------------

class SourceReference(BaseModel):
    """Lien vers un extrait de document source — chaque constat doit citer."""
    doc_id: str
    section: Optional[str] = None
    page: Optional[int] = None
    snippet: str
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)


# ---------------------------------------------------------------------------
# Constats & Risques
# ---------------------------------------------------------------------------

class Finding(BaseModel):
    id: str
    agent_id: str
    category: str
    description: str
    severity: Severity
    sources: List[SourceReference]
    tags: List[str] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Risk(BaseModel):
    id: str
    agent_id: str
    title: str
    description: str
    impact: Severity
    probability: Probability
    mitigations: List[str]
    sources: List[SourceReference]
    dependencies: List[str] = []


# ---------------------------------------------------------------------------
# Recommandations & Priorisation
# ---------------------------------------------------------------------------

class Recommendation(BaseModel):
    id: str
    agent_id: str
    title: str
    description: str
    effort: Effort
    impact: Impact
    timeframe: Timeframe
    priority_score: Optional[float] = None
    dependencies: List[str] = []
    sources: List[SourceReference] = []


class QuickWin(BaseModel):
    id: str
    title: str
    description: str
    estimated_weeks: int = Field(ge=1, le=4)
    expected_impact: str
    prerequisites: List[str] = []


class RoadmapItem(BaseModel):
    id: str
    title: str
    description: str
    phase: Timeframe
    dependencies: List[str] = []
    resources_needed: str = ""
    kpis: List[str] = []


# ---------------------------------------------------------------------------
# Maturité & Scoring
# ---------------------------------------------------------------------------

class MaturityScore(BaseModel):
    dimension: str
    score: MaturityLevel
    justification: str
    gaps: List[str]
    sources: List[SourceReference] = []


# ---------------------------------------------------------------------------
# ROI & Scénarios
# ---------------------------------------------------------------------------

class ROIScenario(BaseModel):
    scenario_type: ScenarioType
    capex_estimate: float
    opex_annual: float
    gains_annual: float
    payback_months: float
    assumptions: List[str]
    sensitivity_notes: str = ""


class ROIModel(BaseModel):
    scenarios: List[ROIScenario]
    investment_horizon_months: int = 36
    discount_rate: float = 0.08
    key_hypotheses: List[str] = []


# ---------------------------------------------------------------------------
# Output générique agent
# ---------------------------------------------------------------------------

class AgentOutput(BaseModel):
    """Schema commun que chaque agent DOIT retourner."""
    agent_id: str
    agent_name: str
    findings: List[Finding] = []
    risks: List[Risk] = []
    recommendations: List[Recommendation] = []
    maturity_scores: List[MaturityScore] = []
    metadata: Dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Evidence Map (traçabilité globale)
# ---------------------------------------------------------------------------

class EvidenceMap(BaseModel):
    """Référence croisée : chaque constat/risque/reco → ses sources."""
    finding_sources: Dict[str, List[SourceReference]] = {}
    risk_sources: Dict[str, List[SourceReference]] = {}
    recommendation_sources: Dict[str, List[SourceReference]] = {}
