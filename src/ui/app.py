import streamlit as st
import time
import json
import sys
import os

# Ensure the src folder is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.orchestrator.graph import audit_graph
from src.agents.plugins.ia_readiness import IAReadinessAgent

st.set_page_config(page_title="IAG Audit Factory", page_icon="🏭", layout="wide")

st.title("🏭 IAG Audit Factory - MVP")
st.markdown("Plateforme d'audits clients opérée par une armée d'agents IA.")

st.sidebar.header("Lancement d'un Audit")
audit_type = st.sidebar.selectbox(
    "Type d'Audit",
    ["Audit IA Readiness", "Audit Stratégique Global", "Audit IT & Architecture"]
)

client_name = st.sidebar.text_input("Nom du Client", "Acme Corp")
uploaded_files = st.sidebar.file_uploader("Documents d'Architecture / Logs", accept_multiple_files=True)

start_button = st.sidebar.button("🚀 Lancer l'Audit Factory")

if start_button:
    st.header(f"Audit en cours : {client_name} - {audit_type}")
    
    # Placeholder for the progress UI
    progress_bar = st.progress(0)
    status_text = st.empty()
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Console Agents")
        console_container = st.empty()
        
    with col2:
        st.subheader("Graph State (Données Consolidées)")
        state_container = st.empty()

    # Initial mock state
    docs_list = [f.name for f in uploaded_files] if uploaded_files else ["it_arch_v1.pdf", "interviews_cdos.docx"]
    initial_state = {
        "audit_id": f"AUDIT-2026-{(hash(time.time()) % 10000):04d}",
        "audit_type": audit_type,
        "client_context": {
            "name": client_name,
            "docs_provided": docs_list
        },
        "current_phase": "Init",
        "errors": [],
        "findings": [],
        "risks": [],
        "recommendations": [],
        "dependencies": [],
        "scores": {},
        "roi_model": None,
        "exec_summary": None
    }

    logs = []
    
    # Helper to update UI
    def update_ui(phase_name, progress, current_state):
        logs.append(f"✅ **Phase atteinte:** {phase_name}")
        console_container.markdown("\n\n".join(logs))
        
        # Convert Pydantic objects to dicts for JSON display
        display_state = {}
        for k, v in current_state.items():
            if isinstance(v, list):
                display_state[k] = [item.model_dump() if hasattr(item, "model_dump") else item for item in v]
            elif hasattr(v, "model_dump"):
                display_state[k] = v.model_dump()
            else:
                display_state[k] = v
                
        state_container.json(display_state)
        progress_bar.progress(progress)
        status_text.text(f"Exécution : {phase_name}...")
        # time.sleep(0.5) # Reduced delay for real AI calls

    logs.append(f"🚀 Démarrage du pipeline pour {audit_type}...")
    console_container.markdown("\n\n".join(logs))

    # Run the graph
    step_count = 0
    total_steps = 7

    for event in audit_graph.stream(initial_state):
        for node_name, state_data in event.items():
            step_count += 1
            progress = min(step_count / total_steps, 1.0)
            
            # Sub-agent real injection
            if node_name == "plugin_agents":
                st.toast(f"🤖 Claude Agent Spécialisé activé", icon="🤖")
                logs.append("🤖 *Agent IA Readiness* (Claude) analyse le contexte...")
                agent = IAReadinessAgent()
                plugin_result = agent.analyze(state_data["client_context"])
                state_data["findings"].extend(plugin_result["findings"])
                
            if node_name == "validation":
                st.warning("Validation Humaine requise. (Auto-approuvé)")
                
            update_ui(state_data["current_phase"], progress, state_data)

    st.success("🎉 Audit terminé par Claude avec succès !")
    
    st.markdown("---")
    st.subheader("Livrable : Executive Summary")
    st.info(state_data.get("exec_summary", "Non généré"))
    
    if state_data.get("findings"):
        st.subheader("Découvertes Principales (Findings générés par Claude)")
        display_findings = []
        for f in state_data["findings"]:
            if hasattr(f, "model_dump"):
                f_dict = f.model_dump()
            else:
                f_dict = f
            display_findings.append({
                "Sévérité": f_dict.get("severity"),
                "Catégorie": f_dict.get("category"),
                "Description": f_dict.get("description")
            })
        st.table(display_findings)
