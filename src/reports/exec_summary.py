"""Executive Summary renderer — transforms structured data into Markdown."""

from __future__ import annotations

from typing import Any, Dict


def render_exec_summary(state: Dict[str, Any]) -> str:
    """Generate a Markdown executive summary from the audit state."""
    ctx = state.get("client_context", {})
    audit_type = state.get("audit_type", "N/A")
    findings = state.get("findings", [])
    risks = state.get("risks", [])
    recommendations = state.get("recommendations", [])
    maturity = state.get("maturity_scores", {})
    quick_wins = state.get("quick_wins", [])

    # Top findings by severity
    critical_findings = [f for f in findings if f.get("severity") in ("CRITICAL", "HIGH")]
    top_findings = critical_findings[:5] if critical_findings else findings[:5]

    # Top risks
    critical_risks = [r for r in risks if r.get("impact") in ("CRITICAL", "HIGH")]
    top_risks = critical_risks[:3] if critical_risks else risks[:3]

    # Top recommendations
    top_recos = sorted(
        recommendations,
        key=lambda r: r.get("priority_score", 0),
        reverse=True,
    )[:5]

    md = f"""# {audit_type} — Executive Summary
## Client : {ctx.get('name', 'N/A')} | Industrie : {ctx.get('industry', 'N/A')}

---

## Contexte & Objectifs
{ctx.get('objectives', 'Objectifs non renseignés.')}

---

## Constats Majeurs

"""
    for i, f in enumerate(top_findings, 1):
        md += f"{i}. **[{f.get('severity', '?')}]** {f.get('description', 'N/A')}\n"

    md += "\n---\n\n## Risques Critiques\n\n"
    for i, r in enumerate(top_risks, 1):
        md += f"{i}. **{r.get('title', 'N/A')}** (Impact: {r.get('impact', '?')}, Probabilité: {r.get('probability', '?')})\n"
        md += f"   - {r.get('description', '')}\n"

    md += "\n---\n\n## Recommandations Prioritaires\n\n"
    for i, rec in enumerate(top_recos, 1):
        md += f"{i}. **{rec.get('title', 'N/A')}** — {rec.get('timeframe', '?')} (Effort: {rec.get('effort', '?')})\n"
        md += f"   - {rec.get('description', '')}\n"

    if maturity:
        md += "\n---\n\n## Maturité par Dimension\n\n"
        md += "| Dimension | Score (1-5) |\n|---|---|\n"
        for dim, data in maturity.items():
            score = data.get("score", "?") if isinstance(data, dict) else data
            md += f"| {dim} | {score} |\n"

    if quick_wins:
        md += "\n---\n\n## Quick Wins (2-4 semaines)\n\n"
        for qw in quick_wins:
            md += f"- **{qw.get('title', 'N/A')}** ({qw.get('estimated_weeks', '?')} sem.) : {qw.get('description', '')}\n"

    md += "\n---\n\n## Prochaines Étapes\n\n"
    md += "1. Valider les constats avec les parties prenantes\n"
    md += "2. Prioriser les quick wins pour démarrage immédiat\n"
    md += "3. Planifier la roadmap 3/6/12 mois\n"
    md += "4. Définir la gouvernance de suivi\n"

    return md
