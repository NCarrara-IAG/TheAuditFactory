from src.agents.core.prompts import PLUGIN_PATTERN_PROMPT

class IAReadinessAgent:
    def __init__(self):
        self.plugin_name = "IA Readiness Evaluator"
        self.directives = "Maturité data, cas d'usage IA, ROI potentiel, gouvernance IA"
        self.prompt = PLUGIN_PATTERN_PROMPT.format(
            plugin_name=self.plugin_name,
            directives=self.directives
        )

    def analyze(self, context: dict):
        # Mocking an agent response based on the plugin prompt
        print(f"[{self.plugin_name}] Analyzing based on directives: {self.directives}")
        return {
            "findings": [
                {
                    "id": "f_ia_1",
                    "category": "Data Governance",
                    "description": "Lack of centralized data warehouse limits immediate AI model training.",
                    "severity": "HIGH",
                    "sources": [{"doc_id": "it_arch_v1.pdf", "snippet": "Data silos exist across 3 main departments."}]
                }
            ]
        }
