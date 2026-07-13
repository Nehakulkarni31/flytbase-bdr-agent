from tools.llm_client import LLMClient

class EmailGenerator:
    def __init__(self):
        self.llm = LLMClient()

    def run(self, contacts: list, research_data: list, brief: dict = None) -> list:
        print("✍️ Generating contextual outbound emails...")
        emails = []
        
        for contact in contacts:
            # Match the research signal to the contact's company
            company = contact.get('company_name', 'Unknown Company')
            signal = next((r['signal'] for r in research_data if r['account_id'] == contact['account_id']), "No specific news found.")
            
            system_prompt = """You are an elite enterprise BDR writing cold outbound emails to LatAm mining executives. 
            
            Strict Behavioral Rules:
            1. NO TEMPLATES: Tie the operational research signal directly to the contact's role.
            2. MATCH THE INDUSTRY: Weave in a reference customer organically, but it MUST match their industry. If they are in Mining, mention Anglo American. NEVER mention Shell to a mining company.
            3. STRUCTURE: 
               - Greeting: "Hi [First Name],"
               - Body: Max 3 short sentences.
               - CTA: End with a specific, low-friction question (e.g., "Worth 15 minutes to see if this fits how you currently handle site inspections?").
            4. SUBJECT LINE: Must be casual and sentence case.
            
            Output strict JSON:
            {"subject": "...", "draft_body": "..."}
            """
            
            user_prompt = f"Prospect: {contact.get('name', 'Leader')}, Title: {contact.get('title', 'Executive')} at {company}.\nResearch Signal: {signal}"
            
            try:
                extracted = self.llm.generate_json(system_prompt, user_prompt)
                
                # POST-HOC PYTHON ENFORCEMENT
                # Force subject line to lowercase and strip stray quotes
                final_subject = extracted.get("subject", "").lower().strip('"').strip("'")
                final_body = extracted.get("draft_body", "")
                
                # Programmatically check word count
                word_count = len(final_body.split())
                if word_count > 80:
                    print(f"      [!] Warning: Draft for {company} exceeded word count ({word_count} words).")
                
                # Merge all data down the pipeline so the review queue can see it
                merged_draft = {**contact, "subject": final_subject, "draft_body": final_body, "source_signal_used": signal}
                emails.append(merged_draft)
                
            except Exception as e:
                print(f"❌ EmailGenerator Failed for {company}: {e}")
                
        return emails