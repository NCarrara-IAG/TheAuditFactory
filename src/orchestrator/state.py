"""AuditGraphState — the single source of truth flowing through the pipeline.

Uses LangGraph's Annotated reducers so that parallel agent nodes can
independently append findings/risks/recommendations which get merged
automatically when the graph reconverges.
"""

from __future__ import annotations

import operator
from typing import Annotated, Any, Dict, List, Optional, TypedDict


class AuditGraphState(TypedDict):
    # ── Identity ──────────────────────────────────────────────────────────
    audit_id: str
    audit_type: str                       # AuditType enum value
    input_hash: str                       # SHA-256 of inputs for idempotency

    # ── Client Context ────────────────────────────────────────────────────
    client_context: Dict[str, Any]
    # Expected keys: name, industry, size, objectives, constraints,
    #                docs_provided (list of doc ids)

    # ── Sources & RAG ─────────────────────────────────────────────────────
    sources_index: Dict[str, Any]         # doc_id -> {name, type, chunks_count, …}
    extracted_entities: List[Dict[str, Any]]

    # ── Pipeline Tracking ─────────────────────────────────────────────────
    current_phase: str                    # AuditPhase enum value
    active_agents: List[str]
    errors: Annotated[List[str], operator.add]
    token_usage: Dict[str, int]           # agent_id -> tokens consumed
    execution_timeline: Annotated[List[Dict[str, Any]], operator.add]
    # Each entry: {agent_id, node, started_at, ended_at, status, tokens}

    # ── Agent Outputs (accumulated via reducer) ───────────────────────────
    findings: Annotated[List[Dict[str, Any]], operator.add]
    risks: Annotated[List[Dict[str, Any]], operator.add]
    recommendations: Annotated[List[Dict[str, Any]], operator.add]

    # ── Scoring ───────────────────────────────────────────────────────────
    maturity_scores: Dict[str, Any]
    # dimension -> {score: int, justification: str, gaps: list}

    # ── ROI ───────────────────────────────────────────────────────────────
    roi_model: Optional[Dict[str, Any]]

    # ── Prioritized Outputs ───────────────────────────────────────────────
    quick_wins: List[Dict[str, Any]]
    roadmap: List[Dict[str, Any]]
    scenarios: List[Dict[str, Any]]       # 3 trajectory scenarios

    # ── Evidence & Traceability ───────────────────────────────────────────
    evidence_map: Dict[str, Any]
    # finding_id/risk_id/reco_id -> [SourceReference dicts]

    # ── Human Checkpoint ──────────────────────────────────────────────────
    human_validated: bool
    human_overrides: Dict[str, Any]

    # ── Final Deliverables ────────────────────────────────────────────────
    exec_summary: Optional[str]
    slides_content: Optional[List[Dict[str, Any]]]
    roadmap_content: Optional[Dict[str, Any]]


def build_initial_state(
    audit_id: str,
    audit_type: str,
    client_context: Dict[str, Any],
    input_hash: str = "",
) -> AuditGraphState:
    """Factory for a clean initial state."""
    return AuditGraphState(
        audit_id=audit_id,
        audit_type=audit_type,
        input_hash=input_hash,
        client_context=client_context,
        sources_index={},
        extracted_entities=[],
        current_phase="init",
        active_agents=[],
        errors=[],
        token_usage={},
        execution_timeline=[],
        findings=[],
        risks=[],
        recommendations=[],
        maturity_scores={},
        roi_model=None,
        quick_wins=[],
        roadmap=[],
        scenarios=[],
        evidence_map={},
        human_validated=False,
        human_overrides={},
        exec_summary=None,
        slides_content=None,
        roadmap_content=None,
    )
