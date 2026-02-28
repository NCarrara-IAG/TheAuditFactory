"""Tests for agent output validation and router logic."""

import pytest

from src.orchestrator.router import (
    CORE_AGENT_IDS,
    resolve_agents_for_audit,
    get_maturity_dimensions,
)
from src.schemas.enums import AuditType
from src.agents.base import BaseAgent
from src.schemas.models import AgentOutput
from src.agents.plugins.registry import get_plugin_agents


# ─── Router ───────────────────────────────────────────────────────────────

class TestRouter:
    def test_core_agents_always_4(self):
        assert len(CORE_AGENT_IDS) == 4

    def test_resolve_ia_readiness(self):
        core, plugins = resolve_agents_for_audit(AuditType.IA_READINESS.value)
        assert core == CORE_AGENT_IDS
        assert "ia_readiness" in plugins

    def test_resolve_it_architecture(self):
        core, plugins = resolve_agents_for_audit(AuditType.IT_ARCHITECTURE.value)
        assert "it_architecture_evaluator" in plugins
        assert "cloud_cost_analyzer" in plugins

    def test_maturity_dimensions_not_empty(self):
        for at in AuditType:
            dims = get_maturity_dimensions(at.value)
            assert len(dims) > 0, f"No maturity dimensions for {at}"

    def test_all_audit_types_resolvable(self):
        for at in AuditType:
            core, plugins = resolve_agents_for_audit(at.value)
            assert len(core) == 4
            assert len(plugins) >= 1


# ─── Plugin Registry ─────────────────────────────────────────────────────

class TestPluginRegistry:
    def test_get_ia_readiness_plugin(self):
        agents = get_plugin_agents(["ia_readiness"])
        assert len(agents) == 1
        assert agents[0].agent_id == "ia_readiness"

    def test_deduplication(self):
        agents = get_plugin_agents(["ia_readiness", "mlops_readiness_agent"])
        assert len(agents) == 1  # same class, deduplicated

    def test_unknown_plugin_skipped(self):
        agents = get_plugin_agents(["nonexistent_plugin"])
        assert len(agents) == 0


# ─── BaseAgent ────────────────────────────────────────────────────────────

class TestBaseAgent:
    def test_parse_output_valid_json(self):
        class DummyAgent(BaseAgent):
            def run(self, state):
                return AgentOutput(agent_id=self.agent_id, agent_name=self.agent_name)

        agent = DummyAgent("test", "Test", "prompt")
        output = agent.parse_output('{"findings": [], "risks": []}')
        assert output.agent_id == "test"
        assert output.findings == []

    def test_parse_output_invalid_json(self):
        class DummyAgent(BaseAgent):
            def run(self, state):
                return AgentOutput(agent_id=self.agent_id, agent_name=self.agent_name)

        agent = DummyAgent("test", "Test", "prompt")
        output = agent.parse_output("not json at all")
        assert output.agent_id == "test"
        assert "parse_error" in output.metadata
