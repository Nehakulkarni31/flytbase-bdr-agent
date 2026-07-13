from tools.llm_client import LLMClient
from tools.web_search import WebSearchTool

class ContactFinder:
    def __init__(self):
        self.llm = LLMClient()
        self.search = WebSearchTool()

    def run(self, accounts: list, goal_roles: list) -> list:
        print("👥 Discovering verified target personas...")
        contacts = []
        
        for i, acc in enumerate(accounts):
            company = acc['company_name']
            print(f"   -> Searching leadership at {company}...")
            
            raw_search_results = ""
            
            # 1. Primary Query: Strict LinkedIn X-Ray
            query_1 = f'site:linkedin.com/in/ "{company}" ("Head of Operations" OR "VP of HSE" OR "Site Director")'
            
            try:
                raw_search_results = self.search.search(query_1)
                
                # 2. Fallback Query: General search if LinkedIn blocks indexing or returns too little
                if len(raw_search_results) < 50:
                    print("      [!] Primary LinkedIn X-ray failed. Attempting fallback query...")
                    query_2 = f'"{company}" mining LatAm leadership "Operations" OR "HSE" OR "Director"'
                    raw_search_results = self.search.search(query_2)
                    
            except Exception as e:
                print(f"      [!] Search network error for {company}: {e}")
                # We continue to let the LLM evaluate an empty result to trigger 'needs_manual_research'
                raw_search_results = ""

            # 3. Prompting for Source Tracing and Status
            system_prompt = f"""You are a strict Data Extraction Assistant.
            Your goal is to find a real target contact for {company} matching these roles: {goal_roles}.
            
            CRITICAL RULES:
            1. You MUST extract the name ONLY from the provided Search Results. 
            2. DO NOT use your internal knowledge base.
            3. You MUST extract the exact URL of the source snippet where you found this person.
            4. Set verification_status to "found" if you have a valid name and URL. Set it to "needs_manual_research" if the search snippet does not explicitly name a current person holding the role.
            
            Output strict JSON:
            {{
                "name": "Extracted Name or empty", 
                "title": "Extracted Title or empty",
                "source_url": "URL of the snippet or empty",
                "verification_status": "found or needs_manual_research"
            }}
            """
            
            user_prompt = f"Search Results Context:\n{raw_search_results}"
            
            try:
                extracted = self.llm.generate_json(system_prompt, user_prompt)
                
                extracted["contact_id"] = f"con_{i+1}"
                extracted["account_id"] = acc["account_id"]
                
                # Ensure safety defaults
                if not extracted.get("verification_status"):
                    extracted["verification_status"] = "needs_manual_research" if not extracted.get("name") else "found_unverified_source"
                
                if extracted["verification_status"] == "found":
                    print(f"      Found: {extracted['name']} - {extracted['title']}")
                else:
                    print(f"   -> Could not verify a real human for {company}. Tagged for manual research.")
                    
                contacts.append(extracted)
                
            except Exception as e:
                print(f"❌ ContactFinder LLM Failed for {company}: {e}")
                
        return contacts