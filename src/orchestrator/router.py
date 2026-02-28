"""Route audit types to the correct set of agents.

The router reads the AuditTypeConfig catalogue and returns the list of
core agents (always activated) + plugin agents (per audit type).
"""

from __future__ import annotations

from typing import List, Tuple

from src.schemas.enums import AuditType
from src.schemas.audit_types import AUDIT_CATALOGUE, AuditTypeConfig

# Core agents run on EVERY audit — they are transversal.
CORE_AGENT_IDS: List[str] = [
    "data_scanner",
    "process_mapper",
    "benchmark",
    "risk_compliance",
]

# Post-analysis agents (sequential, after consolidation)
POST_ANALYSIS_AGENT_IDS: List[str] = [
    "roi_modeler",
    "prioritization",
    "report_generator",
]


def resolve_agents_for_audit(audit_type: str) -> Tuple[List[str], List[str]]:
    """Return (core_agents, plugin_agents) for the given audit type.

    core_agents always includes the 4 transversal agents.
    plugin_agents depends on the audit type catalogue.
    """
    at = AuditType(audit_type)
    config: AuditTypeConfig = AUDIT_CATALOGUE[at]
    return CORE_AGENT_IDS, config.plugin_agents


def get_maturity_dimensions(audit_type: str) -> List[str]:
    """Return the list of maturity dimensions to score for this audit type."""
    at = AuditType(audit_type)
    return AUDIT_CATALOGUE[at].maturity_dimensions
