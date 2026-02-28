"""Slides renderer — generates structured slide content as JSON/Markdown.

The output can be converted to PPTX using python-pptx or fed into
a template engine.
"""

from __future__ import annotations

from typing import Any, Dict, List

from src.schemas.enums import AUDIT_TYPE_LABELS, AuditType


def render_slides(state: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate slide content from the audit state.

    Returns a list of slide dicts compatible with SlideContent schema.
    """
    ctx = state.get("client_context", {})
    client_name = ctx.get("name", "Client")
    audit_type = state.get("audit_type", "")
    audit_label = AUDIT_TYPE_LABELS.get(AuditType(audit_type), audit_type)

    findings = state.get("findings", [])
    risks = state.get("risks", [])
    recommendations = state.get("recommendations", [])
    maturity = state.get("maturity_scores", {})
    quick_wins = state.get("quick_wins", [])
    scenarios = state.get("scenarios", [])
    roi = state.get("roi_model", {})

    slides = []

    # Slide 1: Cover
    slides.append({
        "slide_number": 1,
        "title": f"{audit_label}",
        "layout": "title_only",
        "bullets": [client_name, "iag-services.ai", "Confidentiel"],
        "speaker_notes": "Slide de couverture",
    })

    # Slide 2: Context
    slides.append({
        "slide_number": 2,
        "title": "Contexte & Objectifs",
        "layout": "title_content",
        "bullets": [
            f"Client : {client_name}",
            f"Industrie : {ctx.get('industry', 'N/A')}",
            f"Objectifs : {ctx.get('objectives', 'N/A')}",
        ],
        "speaker_notes": "Rappel du contexte de la mission",
    })

    # Slide 3: Methodology
    slides.append({
        "slide_number": 3,
        "title": "Méthodologie IAG Audit Factory",
        "layout": "title_content",
        "bullets": [
            "Pipeline multi-agents orchestré par IA",
            "Analyse automatisée + validation humaine",
            "Scoring maturité sur dimensions clés",
            "3 scénarios de trajectoire chiffrés",
        ],
        "speaker_notes": "Expliquer la méthodologie différenciante",
    })

    # Slide 4: Key Findings
    top_findings = sorted(
        findings,
        key=lambda f: {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}.get(f.get("severity", "LOW"), 0),
        reverse=True,
    )[:5]
    slides.append({
        "slide_number": 4,
        "title": "Constats Majeurs",
        "layout": "title_content",
        "bullets": [
            f"[{f.get('severity')}] {f.get('description', '')[:100]}"
            for f in top_findings
        ],
        "speaker_notes": f"{len(findings)} constats au total",
    })

    # Slide 5: Maturity Radar
    slides.append({
        "slide_number": 5,
        "title": "Cartographie Maturité",
        "layout": "chart",
        "bullets": [],
        "chart_data": {
            "type": "radar",
            "labels": list(maturity.keys()),
            "values": [
                (d.get("score", 0) if isinstance(d, dict) else d)
                for d in maturity.values()
            ],
        },
        "speaker_notes": "Radar chart des scores de maturité par dimension",
    })

    # Slide 6: Risk Matrix
    slides.append({
        "slide_number": 6,
        "title": "Matrice des Risques",
        "layout": "title_content",
        "bullets": [
            f"{r.get('title', 'N/A')} — Impact: {r.get('impact')}, Proba: {r.get('probability')}"
            for r in risks[:6]
        ],
        "speaker_notes": f"{len(risks)} risques identifiés",
    })

    # Slide 7: Top Recommendations
    slides.append({
        "slide_number": 7,
        "title": "Recommandations Prioritaires",
        "layout": "title_content",
        "bullets": [
            f"{r.get('title', 'N/A')} ({r.get('timeframe', '?')})"
            for r in recommendations[:6]
        ],
        "speaker_notes": f"{len(recommendations)} recommandations au total",
    })

    # Slide 8: Quick Wins
    slides.append({
        "slide_number": 8,
        "title": "Quick Wins (2-4 semaines)",
        "layout": "title_content",
        "bullets": [
            f"{qw.get('title', 'N/A')} — {qw.get('estimated_weeks', '?')} sem."
            for qw in quick_wins
        ],
        "speaker_notes": "Actions à démarrer immédiatement",
    })

    # Slide 9: Scenarios
    for sc in scenarios:
        slides.append({
            "slide_number": len(slides) + 1,
            "title": f"Scénario {sc.get('scenario_type', '').title()}",
            "layout": "title_content",
            "bullets": sc.get("key_actions", [])[:5],
            "speaker_notes": sc.get("description", ""),
        })

    # Slide 10+: ROI
    if roi and roi.get("scenarios"):
        roi_bullets = []
        for rs in roi["scenarios"]:
            roi_bullets.append(
                f"{rs.get('scenario_type', '').title()}: "
                f"CAPEX {rs.get('capex_estimate', 0):,.0f}€, "
                f"Payback {rs.get('payback_months', 0):.0f} mois"
            )
        slides.append({
            "slide_number": len(slides) + 1,
            "title": "Estimation ROI",
            "layout": "title_content",
            "bullets": roi_bullets,
            "speaker_notes": "3 scénarios financiers",
        })

    # Last slide: Next Steps
    slides.append({
        "slide_number": len(slides) + 1,
        "title": "Prochaines Étapes",
        "layout": "title_content",
        "bullets": [
            "Validation des constats avec les parties prenantes",
            "Lancement des quick wins",
            "Cadrage roadmap 3/6/12 mois",
            "Gouvernance de suivi et KPIs",
        ],
        "speaker_notes": "Clôture et call to action",
    })

    return slides
