import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from src.orchestrator.graph import audit_graph

def export_graph():
    # Generate the Mermaid diagram
    mermaid_str = audit_graph.get_graph().draw_mermaid()
    
    # Save the mermaid code to a file
    with open("langgraph_architecture.md", "w") as f:
        f.write("# LangGraph Execution Architecture\n\n```mermaid\n")
        f.write(mermaid_str)
        f.write("\n```\n")
    
    # Attempt to save PNG (Requires internet connection to Mermaid's API)
    try:
        png_data = audit_graph.get_graph().draw_mermaid_png()
        with open("langgraph_architecture.png", "wb") as f:
            f.write(png_data)
        print("Successfully exported langgraph_architecture.png")
    except Exception as e:
        print(f"Failed to export PNG: {e}")

if __name__ == "__main__":
    export_graph()
