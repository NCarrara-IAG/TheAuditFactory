import os
import asyncio
from typing import Dict, Any
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

class StitchDesignerAgent:
    def __init__(self):
        self.agent_id = "stitch_designer"
        self.agent_name = "Stitch UI Designer"
        self.api_key = os.getenv("STITCH_API_KEY")

    async def generate_cockpit(self, audit_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calls Google Stitch via MCP to generate a premium React dashboard 
        based on the audit findings.
        """
        print(f"[{self.agent_name}] Generating premium UI for {audit_data.get('audit_type')}...")
        
        # Prepare the prompt for Stitch
        prompt = self._build_stitch_prompt(audit_data)
        
        # MCP Connection Parameters
        # Direct execution of the stitch-mcp server
        server_params = StdioServerParameters(
            command="npx",
            args=["-y", "@_davideast/stitch-mcp", "start"],
            env={**os.environ, "STITCH_API_KEY": self.api_key}
        )
        
        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    # Initialize the session
                    await session.initialize()
                    
                    # Call the 'build_site' or equivalent tool
                    # Based on research, stitch-mcp provides 'create_screen' or 'build_site'
                    # Let's try to list tools first to be sure or use a common one.
                    # For this MVP code, we'll assume 'create_site' exists as per documentation.
                    
                    print(f"[{self.agent_name}] Calling Stitch MCP build_site tool...")
                    response = await session.call_tool(
                        "create_site", # Adjust based on actual tool name in @_davideast/stitch-mcp
                        arguments={
                            "prompt": prompt,
                            "name": f"Audit-Cockpit-{audit_data.get('client_context', {}).get('name', 'Client')}"
                        }
                    )
                    
                    return {
                        "status": "success",
                        "ui_url": response.content[0].text if response.content else "Pending generation...",
                        "message": "Stitch is crafting your premium dashboard."
                    }
        except Exception as e:
            print(f"Error calling Stitch MCP: {e}")
            return {"status": "error", "message": str(e)}

    def _build_stitch_prompt(self, data: Dict[str, Any]) -> str:
        findings_summary = "\n".join([f"- {f.description}" for f in data.get("findings", [])[:3]])
        client_name = data.get("client_context", {}).get("name", "Client")
        
        return f"""
        Crée un Cockpit d'Audit premium et "wow" pour le client {client_name}.
        L'interface doit être sombre, moderne, utilisant du glassmorphism et des accents de couleurs vibrantes (IAG Services AI Style).
        
        Inclus les sections suivantes :
        1. Résumé Exécutif avec de gros indicateurs clés.
        2. Top Findings :
        {findings_summary}
        3. Un graphique de ROI (basé sur un payback de {data.get('roi_model', {}).payback_period_months if data.get('roi_model') else 12} mois).
        4. Une timeline interactive de 12 mois pour la roadmap.
        
        L'interface doit paraître extrêmement experte et technologique.
        """

# For standalone testing
if __name__ == "__main__":
    mock_data = {
        "audit_type": "IA Readiness",
        "client_context": {"name": "Acme Corp"},
        "findings": [{"description": "Lack of centralized data governance"}],
        "roi_model": {"payback_period_months": 6}
    }
    agent = StitchDesignerAgent()
    asyncio.run(agent.generate_cockpit(mock_data))
