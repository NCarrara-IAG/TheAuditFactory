"""Schemas for final deliverables generated at the end of the audit pipeline."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .enums import ScenarioType, Timeframe
from .models import (
    Finding,
    MaturityScore,
    QuickWin,
    Risk,
    ROIModel,
    RoadmapItem,
    Recommendation,
)


class SlideContent(BaseModel):
    """One slide in the restitution deck."""
    slide_number: int
    title: str
    layout: str = "title_content"  # title_only, title_content, two_column, chart
    bullets: List[str] = []
    chart_data: Optional[Dict[str, Any]] = None
    speaker_notes: str = ""


class ExecSummaryDeliverable(BaseModel):
    """1-2 page executive summary."""
    title: str
    client_name: str
    audit_type_label: str
    date: str
    context_paragraph: str
    key_findings: List[str]
    critical_risks: List[str]
    top_recommendations: List[str]
    maturity_overview: Dict[str, int]  # dimension -> score 1-5
    next_steps: List[str]


class RoadmapDeliverable(BaseModel):
    """Roadmap 3/6/12 mois."""
    quick_wins: List[QuickWin]
    three_months: List[RoadmapItem]
    six_months: List[RoadmapItem]
    twelve_months: List[RoadmapItem]


class TrajectoryScenario(BaseModel):
    """Un des 3 scénarios de trajectoire."""
    scenario_type: ScenarioType
    label: str
    description: str
    key_actions: List[str]
    expected_maturity_gains: Dict[str, int]  # dimension -> target score
    investment_range: str
    timeline: str
    risks: List[str]


class AuditDeliverableBundle(BaseModel):
    """Le bundle complet de livrables d'un audit."""
    audit_id: str
    exec_summary: ExecSummaryDeliverable
    slides: List[SlideContent]
    roadmap: RoadmapDeliverable
    scenarios: List[TrajectoryScenario]
    roi_model: ROIModel
    all_findings: List[Finding]
    all_risks: List[Risk]
    all_recommendations: List[Recommendation]
    maturity_scores: List[MaturityScore]
