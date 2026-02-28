"""Plugin agent registry — maps plugin IDs to their agent classes.

Adding a new plugin agent:
1. Create a new file in src/agents/plugins/
2. Inherit from BaseAgent
3. Register it in PLUGIN_REGISTRY below
"""

from __future__ import annotations

from typing import Dict, List, Type

from src.agents.base import BaseAgent


def _lazy_registry() -> Dict[str, Type[BaseAgent]]:
    """Lazy imports to avoid circular dependencies."""
    from src.agents.plugins.ia_readiness import IAReadinessPlugin
    from src.agents.plugins.smart_factory import SmartFactoryPlugin
    from src.agents.plugins.it_architecture import ITArchitecturePlugin
    from src.agents.plugins.product_delivery import ProductDeliveryPlugin

    return {
        "ia_readiness": IAReadinessPlugin,
        "mlops_readiness_agent": IAReadinessPlugin,  # alias — same plugin covers both
        "smart_factory_evaluator": SmartFactoryPlugin,
        "ot_it_integration_evaluator": SmartFactoryPlugin,
        "it_architecture_evaluator": ITArchitecturePlugin,
        "cloud_cost_analyzer": ITArchitecturePlugin,
        "product_delivery_evaluator": ProductDeliveryPlugin,
        "time_to_market_analyzer": ProductDeliveryPlugin,
        "product_innovation_analyst": ProductDeliveryPlugin,
        "strategic_global_analyst": IAReadinessPlugin,  # placeholder
        "stack_redundancy_detector": ITArchitecturePlugin,
        "poc_failure_analyzer": IAReadinessPlugin,  # placeholder
        "scale_readiness_evaluator": IAReadinessPlugin,  # placeholder
        "iot_readiness_evaluator": SmartFactoryPlugin,
    }


def get_plugin_agents(plugin_ids: List[str]) -> List[BaseAgent]:
    """Instantiate the requested plugin agents, deduplicating by class."""
    registry = _lazy_registry()
    seen_classes = set()
    agents = []
    for pid in plugin_ids:
        cls = registry.get(pid)
        if cls and cls not in seen_classes:
            agents.append(cls())
            seen_classes.add(cls)
    return agents
