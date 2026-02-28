import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from src.orchestrator.state import AuditGraphState
from src.schemas.models import Finding, Risk, Recommendation, ROIModel
from src.agents.core.prompts import (
    ORCHESTRATOR_PROMPT, 
    DATA_SCANNER_PROMPT, 
    REPORT_GENERATOR_PROMPT,
    ROI_MODELER_PROMPT
)

# Load environment variables
load_dotenv()

# Initialize LLM
# Ensure ANTHROPIC_API_KEY is in .env or environment
llm = ChatAnthropic(model="claude-3-5-sonnet-latest", temperature=0)

def node_intake_orchestrator(state: AuditGraphState):
    print(f"[Intake] Processing context for {state['audit_type']}")
    state["current_phase"] = "Intake"
    # Logic to initialize state if empty
    if not state.get("findings"): state["findings"] = []
    if not state.get("errors"): state["errors"] = []
    if not state.get("risks"): state["risks"] = []
    if not state.get("recommendations"): state["recommendations"] = []
    if not state.get("scores"): state["scores"] = {}
    return state

def node_parallel_core_agents(state: AuditGraphState):
    print("[Core Agents] Running Data Scanner via Claude...")
    
    structured_llm = llm.with_structured_output(Finding)
    try:
        # Example: Just one finding for demo, in prod we'd use a loop or Batch
        finding = structured_llm.invoke([
            ("system", DATA_SCANNER_PROMPT),
            ("human", f"Context: {state['client_context']}")
        ])
        state["findings"].append(finding)
    except Exception as e:
        state["errors"].append(f"DataScanner Error: {str(e)}")
        
    state["current_phase"] = "Core Analysis"
    return state

def node_parallel_plugin_agents(state: AuditGraphState):
    print(f"[Plugin Agents] Running plugins for {state['audit_type']}...")
    # Plugins usually have their own specialized logic, but can use the shared LLM
    state["current_phase"] = "Plugin Analysis"
    return state

def node_consolidation_orchestrator(state: AuditGraphState):
    print("[Consolidation] Orchestrator merging findings...")
    state["current_phase"] = "Consolidation"
    return state

def node_roi_prioritization(state: AuditGraphState):
    print("[ROI & Priority] Calculating impact and effort via Claude...")
    structured_roi = llm.with_structured_output(ROIModel)
    try:
        # Pass existing findings to the ROI modeller
        findings_text = "\n".join([f.description for f in state["findings"]])
        roi = structured_roi.invoke([
            ("system", ROI_MODELER_PROMPT),
            ("human", f"Findings actuels:\n{findings_text}")
        ])
        state["roi_model"] = roi
    except Exception as e:
        state["errors"].append(f"ROI Modeler Error: {str(e)}")
        
    state["current_phase"] = "ROI & Priority"
    return state

def node_human_validation(state: AuditGraphState):
    print("[Human Validation] Checkpoint reached.")
    state["current_phase"] = "Validation"
    return state

def node_report_generator(state: AuditGraphState):
    print("[Report Generator] Compiling Executive Summary via Claude...")
    
    try:
        # Generate a real summary based on the findings and ROI
        response = llm.invoke([
            ("system", REPORT_GENERATOR_PROMPT),
            ("human", f"Data: {state}")
        ])
        state["exec_summary"] = response.content
    except Exception as e:
        state["errors"].append(f"Report Generator Error: {str(e)}")
        state["exec_summary"] = "# Error in generation\nPlease check logs."
        
    state["current_phase"] = "Reporting"
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

# Compile
audit_graph = workflow.compile()
