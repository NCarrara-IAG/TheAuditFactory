import json
from src.orchestrator.graph import audit_graph
from src.agents.plugins.ia_readiness import IAReadinessAgent

def run_mock_audit():
    # 1. Input mock
    initial_state = {
        "audit_id": "AUDIT-2026-001",
        "audit_type": "Audit IA Readiness",
        "client_context": {
            "name": "Acme Corp",
            "industry": "Manufacturing",
            "docs_provided": ["it_arch_v1.pdf", "interviews_cdos.docx"]
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
    
    print("--- STARTING AUDIT GRAPH ---")
    
    # Run the graph
    for event in audit_graph.stream(initial_state):
        for k, v in event.items():
            if k == "plugin_agents":
                # Mocking the interaction with the plugin agent
                agent = IAReadinessAgent()
                plugin_result = agent.analyze(v["client_context"])
                v["findings"].extend(plugin_result["findings"])
            print(f"Update from node '{k}': Phase is now {v['current_phase']}")
            
            # Print findings if added
            if k == "plugin_agents" and v["findings"]:
                print(f"  -> Added Findings: {json.dumps(v['findings'], indent=2)}")

    print("\n--- FINAL STATE ---")
    # In a real app we would query the state, but stream returns the last state at the end
    print(f"Executive Summary generated: {v.get('exec_summary')}")
    print(f"Total Findings: {len(v['findings'])}")

if __name__ == "__main__":
    run_mock_audit()
