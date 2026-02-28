"""Roadmap renderer — transforms prioritized recommendations into a structured roadmap."""

from __future__ import annotations

from typing import Any, Dict, List


def render_roadmap(state: Dict[str, Any]) -> str:
    """Generate a Markdown roadmap from the audit state."""
    quick_wins = state.get("quick_wins", [])
    roadmap_items = state.get("roadmap", [])

    # Group by phase
    phases: Dict[str, List[Dict[str, Any]]] = {
        "QUICK_WIN": [],
        "3_MONTHS": [],
        "6_MONTHS": [],
        "12_MONTHS": [],
    }
    for item in roadmap_items:
        phase = item.get("phase", "12_MONTHS")
        phases.setdefault(phase, []).append(item)

    md = "# Roadmap de Transformation\n\n"

    # Quick Wins
    md += "## Quick Wins (2-4 semaines)\n\n"
    if quick_wins:
        for qw in quick_wins:
            md += f"### {qw.get('title', 'N/A')}\n"
            md += f"- **Durée estimée** : {qw.get('estimated_weeks', '?')} semaines\n"
            md += f"- **Impact attendu** : {qw.get('expected_impact', 'N/A')}\n"
            md += f"- **Description** : {qw.get('description', '')}\n\n"
    else:
        md += "_Aucun quick win identifié._\n\n"

    # Phase headers
    phase_labels = {
        "3_MONTHS": "Horizon 3 Mois",
        "6_MONTHS": "Horizon 6 Mois",
        "12_MONTHS": "Horizon 12 Mois",
    }

    for phase_key, label in phase_labels.items():
        items = phases.get(phase_key, [])
        md += f"## {label}\n\n"
        if items:
            for item in items:
                md += f"### {item.get('title', 'N/A')}\n"
                md += f"- **Description** : {item.get('description', '')}\n"
                deps = item.get("dependencies", [])
                if deps:
                    md += f"- **Dépendances** : {', '.join(deps)}\n"
                md += f"- **Ressources** : {item.get('resources_needed', 'À définir')}\n"
                kpis = item.get("kpis", [])
                if kpis:
                    md += f"- **KPIs** : {', '.join(kpis)}\n"
                md += "\n"
        else:
            md += "_Aucune action planifiée sur cet horizon._\n\n"

    return md
