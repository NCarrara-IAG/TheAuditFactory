from typing import Dict, Any
from langgraph.graph import StateGraph, END
from src.orchestrator.state import AuditGraphState

def node_intake_orchestrator(state: AuditGraphState):
    print(f"[Intake] Processing context for {state['audit_type']}")
    state["current_phase"] = "Intake"
    return state

def node_parallel_core_agents(state: AuditGraphState):
    print("[Core Agents] Running Data Scanner, Process Mapper, Compliance...")
    # Mock behavior
    state["current_phase"] = "Core Analysis"
    return state

def node_parallel_plugin_agents(state: AuditGraphState):
    print(f"[Plugin Agents] Running plugins for {state['audit_type']}...")
    return state

def node_consolidation_orchestrator(state: AuditGraphState):
    print("[Consolidation] Orchestrator merging findings...")
    state["current_phase"] = "Consolidation"
    return state

def node_roi_prioritization(state: AuditGraphState):
    print("[ROI & Priority] Calculating impact and effort...")
    state["current_phase"] = "ROI & Priority"
    return state

def node_human_validation(state: AuditGraphState):
    print("[Human Validation] Checkpoint reached. Waiting for IAG approval...")
    state["current_phase"] = "Validation"
    return state

def node_report_generator(state: AuditGraphState):
    print("[Report Generator] Compiling Executive Summary and Slides...")
    state["current_phase"] = "Reporting"
    state["exec_summary"] = "# Executive Summary\n\nAudit completed successfully."
    return state

# Graph Definition
workflow = StateGraph(AuditGraphState)

# Add Nodes
workflow.add_node("intake", node_intake_orchestrator)
workflow.add_node("core_agents", node_parallel_core_agents)
workflow.add_node("plugin_agents", node_parallel_plugin_agents)
workflow.add_node("consolidation", node_consolidation_orchestrator)
workflow.add_node("roi_priority", node_roi_prioritization)
workflow.add_node("validation", node_human_validation)
workflow.add_node("reporting", node_report_generator)

# Add Edges
workflow.set_entry_point("intake")
workflow.add_edge("intake", "core_agents")
workflow.add_edge("core_agents", "plugin_agents")
workflow.add_edge("plugin_agents", "consolidation")
workflow.add_edge("consolidation", "roi_priority")
workflow.add_edge("roi_priority", "validation")
workflow.add_edge("validation", "reporting")
workflow.add_edge("reporting", END)

# Compile the Graph
# Note: Validation step could be made as a real interrupt using checkpointer in production LangGraph
audit_graph = workflow.compile()
