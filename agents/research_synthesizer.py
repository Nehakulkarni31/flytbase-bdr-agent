from tools.web_search import WebSearchTool
from tools.llm_client import LLMClient

class ResearchSynthesizer:
    def __init__(self):
        self.search = WebSearchTool()
        self.llm = LLMClient()

    def run(self, accounts: list) -> list:
        print("🧠 Synthesizing deep research signals...")
        research_briefs = []
        
        for acc in accounts:
            company = acc["company_name"]
            print(f"   -> Researching {company}...")
            
            query = f"Recent news {company} mining Latin America 2025 2026. Focus on site expansions, safety incidents, or autonomous extraction operations."
            raw_data = self.search.search(query)
            
            if not raw_data:
                continue
                
            system_prompt = """You are an intelligence analyst. Extract ONE highly specific, verifiable operational signal from the raw text. 
            Focus on safety friction, site expansion, or contractor bottlenecks.
            Output strict JSON: {"signal": "specific detail", "source_context": "..."}
            """
            
            user_prompt = f"Raw Data:\n{raw_data}"
            
            try:
                extracted = self.llm.generate_json(system_prompt, user_prompt)
                extracted["account_id"] = acc["account_id"]
                extracted["company_name"] = company
                research_briefs.append(extracted)
            except Exception as e:
                print(f"❌ Research Failed for {company}: {e}")
                
        return research_briefs