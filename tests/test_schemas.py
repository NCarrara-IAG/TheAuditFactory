"""Tests for Pydantic schemas — validates that all models serialize/deserialize correctly."""

import pytest
from datetime import datetime, timezone

from src.schemas.enums import (
    AuditType, Severity, Probability, Effort, Impact, Timeframe,
    MaturityLevel, ScenarioType,
)
from src.schemas.models import (
    SourceReference, Finding, Risk, Recommendation, QuickWin,
    RoadmapItem, MaturityScore, ROIScenario, ROIModel, AgentOutput,
    EvidenceMap,
)
from src.schemas.audit_types import AUDIT_CATALOGUE, get_audit_config
from src.schemas.deliverables import (
    SlideContent, ExecSummaryDeliverable, AuditDeliverableBundle,
)


# ─── SourceReference ──────────────────────────────────────────────────────

class TestSourceReference:
    def test_basic(self):
        ref = SourceReference(doc_id="doc1", snippet="some text")
        assert ref.doc_id == "doc1"
        assert ref.confidence == 1.0
        assert ref.section is None

    def test_full(self):
        ref = SourceReference(
            doc_id="arch_v2.pdf", section="3.1", page=12,
            snippet="Legacy ERP on-prem", confidence=0.85,
        )
        data = ref.model_dump()
        assert data["page"] == 12
        assert data["confidence"] == 0.85


# ─── Finding ──────────────────────────────────────────────────────────────

class TestFinding:
    def test_minimal(self):
        f = Finding(
            id="DS-001", agent_id="data_scanner", category="architecture",
            description="Monolithic ERP", severity=Severity.HIGH,
            sources=[SourceReference(doc_id="d1", snippet="mono")],
        )
        assert f.severity == Severity.HIGH
        assert len(f.sources) == 1

    def test_serialization_roundtrip(self):
        f = Finding(
            id="DS-002", agent_id="data_scanner", category="security",
            description="No encryption at rest", severity=Severity.CRITICAL,
            sources=[SourceReference(doc_id="d1", snippet="plain text storage")],
            tags=["security", "urgent"],
        )
        data = f.model_dump()
        f2 = Finding(**data)
        assert f2.id == f.id
        assert f2.tags == ["security", "urgent"]


# ─── Risk ─────────────────────────────────────────────────────────────────

class TestRisk:
    def test_basic(self):
        r = Risk(
            id="RC-001", agent_id="risk_compliance",
            title="No DPO", description="No data protection officer",
            impact=Severity.HIGH, probability=Probability.MEDIUM,
            mitigations=["Hire DPO"],
            sources=[SourceReference(doc_id="d1", snippet="no DPO")],
        )
        assert r.impact == Severity.HIGH
        assert len(r.mitigations) == 1


# ─── Recommendation ──────────────────────────────────────────────────────

class TestRecommendation:
    def test_basic(self):
        rec = Recommendation(
            id="PM-R001", agent_id="process_mapper",
            title="Automate invoicing", description="Replace manual process",
            effort=Effort.LOW, impact=Impact.HIGH, timeframe=Timeframe.QUICK_WIN,
        )
        assert rec.timeframe == Timeframe.QUICK_WIN


# ─── MaturityScore ────────────────────────────────────────────────────────

class TestMaturityScore:
    def test_basic(self):
        ms = MaturityScore(
            dimension="data_governance", score=MaturityLevel.MANAGED,
            justification="Documented but inconsistent",
            gaps=["No data catalogue", "No ownership model"],
        )
        assert ms.score == 2
        assert len(ms.gaps) == 2


# ─── ROIModel ─────────────────────────────────────────────────────────────

class TestROIModel:
    def test_three_scenarios(self):
        scenarios = [
            ROIScenario(
                scenario_type=st, capex_estimate=50000 * (i + 1),
                opex_annual=20000, gains_annual=80000 * (i + 1),
                payback_months=12 - i * 3,
                assumptions=["Hyp 1"],
            )
            for i, st in enumerate([
                ScenarioType.CONSERVATIVE,
                ScenarioType.TARGET,
                ScenarioType.AMBITIOUS,
            ])
        ]
        roi = ROIModel(scenarios=scenarios, key_hypotheses=["600€/day"])
        assert len(roi.scenarios) == 3
        assert roi.scenarios[0].scenario_type == ScenarioType.CONSERVATIVE


# ─── AgentOutput ──────────────────────────────────────────────────────────

class TestAgentOutput:
    def test_empty(self):
        out = AgentOutput(agent_id="test", agent_name="Test Agent")
        assert out.findings == []
        assert out.metadata == {}

    def test_with_findings(self):
        out = AgentOutput(
            agent_id="ds", agent_name="Data Scanner",
            findings=[Finding(
                id="DS-001", agent_id="ds", category="arch",
                description="test", severity=Severity.LOW,
                sources=[SourceReference(doc_id="d1", snippet="x")],
            )],
        )
        assert len(out.findings) == 1


# ─── AuditCatalogue ──────────────────────────────────────────────────────

class TestAuditCatalogue:
    def test_all_9_types_registered(self):
        assert len(AUDIT_CATALOGUE) == 9

    def test_get_config(self):
        cfg = get_audit_config(AuditType.IA_READINESS)
        assert cfg.level == "B"
        assert "ia_readiness" in cfg.plugin_agents

    def test_strategic_types_are_level_a(self):
        for at in [AuditType.STRATEGIC_GLOBAL, AuditType.STRATEGIC_PRODUCT,
                    AuditType.STRATEGIC_COST, AuditType.STRATEGIC_DATA_IA,
                    AuditType.STRATEGIC_SCALE]:
            cfg = get_audit_config(at)
            assert cfg.level == "A"


# ─── Deliverables ─────────────────────────────────────────────────────────

class TestDeliverables:
    def test_slide_content(self):
        s = SlideContent(
            slide_number=1, title="Cover",
            bullets=["Client", "IAG"], speaker_notes="Intro",
        )
        assert s.layout == "title_content"

    def test_exec_summary(self):
        es = ExecSummaryDeliverable(
            title="Audit IA Readiness", client_name="Acme",
            audit_type_label="IA Readiness", date="2026-02-28",
            context_paragraph="Context", key_findings=["F1"],
            critical_risks=["R1"], top_recommendations=["Rec1"],
            maturity_overview={"data": 3}, next_steps=["Next"],
        )
        assert es.client_name == "Acme"
