"""Example complete audit run — Audit IA Readiness on mock client data.

This demonstrates the full pipeline end-to-end:
1. Build initial state with mock client context
2. Stream the LangGraph pipeline
3. Print results at each phase
4. Display final deliverables
"""

from __future__ import annotations

import logging
import sys
from datetime import datetime, timezone

from src.connectors.local_upload import compute_input_hash
from src.orchestrator.graph import audit_graph
from src.orchestrator.state import build_initial_state
from src.schemas.enums import AuditType

logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)
logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════
# MOCK CLIENT DATA — Acme Corp IA Readiness Audit
# ═══════════════════════════════════════════════════════════════════════════

MOCK_CLIENT_CONTEXT = {
    "name": "Acme Manufacturing Corp",
    "industry": "Manufacturing / Industrial",
    "size": "1200 employés, CA 180M€",
    "objectives": (
        "Évaluer notre capacité à déployer l'IA sur nos lignes de production. "
        "Identifier les quick wins data/IA et construire une roadmap réaliste."
    ),
    "constraints": (
        "Budget IT limité (2.5M€/an), équipe data de 3 personnes, "
        "legacy ERP SAP sur site, pas de data lake centralisé."
    ),
    "docs_provided": [
        "architecture_si_acme_2025.pdf",
        "interview_cdo_transcript.docx",
        "interview_dsi_transcript.docx",
        "export_erp_sap_modules.xlsx",
        "organigramme_dsi.pdf",
        "policy_data_governance_v1.pdf",
    ],
}


def run_mock_audit():
    """Run a full IA Readiness audit on mock data."""
    print("=" * 70)
    print("  IAG AUDIT FACTORY — Audit IA Readiness (Mock Run)")
    print("=" * 70)
    print()

    # Build initial state
    input_hash = compute_input_hash(
        MOCK_CLIENT_CONTEXT,
        MOCK_CLIENT_CONTEXT["docs_provided"],
    )

    initial_state = build_initial_state(
        audit_id=f"AUDIT-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M')}",
        audit_type=AuditType.IA_READINESS.value,
        client_context=MOCK_CLIENT_CONTEXT,
        input_hash=input_hash,
    )

    print(f"Audit ID   : {initial_state['audit_id']}")
    print(f"Type       : {initial_state['audit_type']}")
    print(f"Client     : {MOCK_CLIENT_CONTEXT['name']}")
    print(f"Input Hash : {input_hash[:16]}...")
    print()

    # Stream the pipeline
    final_state = None
    for event in audit_graph.stream(initial_state):
        for node_name, state_update in event.items():
            phase = state_update.get("current_phase", "?")
            print(f"  [{node_name:20s}] → phase: {phase}")

            # Show counts for data-producing nodes
            f_count = len(state_update.get("findings", []))
            r_count = len(state_update.get("risks", []))
            rec_count = len(state_update.get("recommendations", []))
            if f_count or r_count or rec_count:
                print(f"  {'':20s}   +{f_count} findings, +{r_count} risks, +{rec_count} recommendations")

            final_state = state_update

    print()
    print("=" * 70)
    print("  PIPELINE COMPLETE")
    print("=" * 70)
    print()

    if not final_state:
        print("No output produced.")
        return

    # ── Summary ────────────────────────────────────────────────────────
    print(f"Total Findings         : {len(final_state.get('findings', []))}")
    print(f"Total Risks            : {len(final_state.get('risks', []))}")
    print(f"Total Recommendations  : {len(final_state.get('recommendations', []))}")
    print(f"Quick Wins             : {len(final_state.get('quick_wins', []))}")
    print(f"Roadmap Items          : {len(final_state.get('roadmap', []))}")
    print(f"Scenarios              : {len(final_state.get('scenarios', []))}")
    print(f"Human Validated        : {final_state.get('human_validated', False)}")
    print()

    # ── Executive Summary ──────────────────────────────────────────────
    exec_summary = final_state.get("exec_summary")
    if exec_summary:
        print("─" * 70)
        print("EXECUTIVE SUMMARY (first 500 chars):")
        print("─" * 70)
        print(exec_summary[:500])
        print("..." if len(exec_summary) > 500 else "")
        print()

    # ── Slides ─────────────────────────────────────────────────────────
    slides = final_state.get("slides_content", [])
    if slides:
        print("─" * 70)
        print(f"SLIDES ({len(slides)} slides generated):")
        print("─" * 70)
        for s in slides:
            print(f"  Slide {s.get('slide_number', '?')}: {s.get('title', 'N/A')}")
        print()

    # ── Execution Timeline ─────────────────────────────────────────────
    timeline = final_state.get("execution_timeline", [])
    if timeline:
        print("─" * 70)
        print("EXECUTION TIMELINE:")
        print("─" * 70)
        for entry in timeline:
            print(f"  [{entry.get('agent_id', '?'):20s}] "
                  f"node={entry.get('node', '?'):15s} "
                  f"status={entry.get('status', '?')}")
        print()

    print("Done. Audit deliverables ready for export.")


if __name__ == "__main__":
    run_mock_audit()
