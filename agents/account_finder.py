from tools.llm_client import LLMClient
from tools.web_search import WebSearchTool

class AccountFinder:
    def __init__(self):
        self.llm = LLMClient()
        self.search = WebSearchTool()

    def run(self, brief: dict) -> list:
        print("🔍 Searching for lookalike accounts in Latin America...")
        
        # 1. Gather live context
        query = f"Top large scale {brief['vertical']} similar to {brief['reference_account']} currently operating. Return specific company names."
        search_context = self.search.search(query)
        
        # 2. Extract structured JSON via LLM
        system_prompt = """You are an expert BDR Research Assistant. 
        Identify 3 distinct real-world Latin American mining companies from the context that closely match the Reference Account.
        Focus on large-scale copper, lithium, or iron ore producers.
        Output MUST be a JSON object containing an array called "accounts":
        {"accounts": [{"account_id": "acc_1", "company_name": "...", "country": "...", "icp_reasoning": "..."}]}
        """
        
        user_prompt = f"Reference: {brief['reference_account']}\nVertical: {brief['vertical']}\nWeb Context: {search_context}"
        
        try:
            results = self.llm.generate_json(system_prompt, user_prompt)
            return results.get("accounts", [])
        except Exception as e:
            print(f"❌ AccountFinder Failed: {e}")
            return []