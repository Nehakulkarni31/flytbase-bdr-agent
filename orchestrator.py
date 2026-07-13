import os
import json
import yaml
from datetime import datetime

from agents.account_finder import AccountFinder
from agents.contact_finder import ContactFinder
from agents.research_synthesizer import ResearchSynthesizer
from agents.email_generator import EmailGenerator

class OutboundEngine:
    def __init__(self):
        with open("config/campaign_brief.yaml", "r") as f:
            self.brief = yaml.safe_load(f)
            
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.run_dir = f"data/run_{self.run_id}"
        os.makedirs(self.run_dir, exist_ok=True)
        print(f"🚀 Initialized Engine. State will be saved to: {self.run_dir}\n")

    def save_state(self, filename: str, data: list):
        filepath = os.path.join(self.run_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"💾 Saved {len(data)} records to {filename}")

    def execute_pipeline(self):
        print("--- STAGE 1: ACCOUNT IDENTIFICATION ---")
        accounts = AccountFinder().run(self.brief)
        self.save_state("1_accounts.json", accounts)

        print("\n--- STAGE 2: CONTACT DISCOVERY ---")
        contacts = ContactFinder().run(accounts, self.brief['goal_roles'])
        self.save_state("2_contacts.json", contacts)

        print("\n--- STAGE 3: ACCOUNT RESEARCH ---")
        research = ResearchSynthesizer().run(accounts)
        self.save_state("3_research.json", research)

        print("\n--- STAGE 4: EMAIL GENERATION ---")
        drafts = EmailGenerator().run(contacts, research, self.brief)
        self.save_state("4_emails.json", drafts)
        
        print(f"\n✅ Pipeline complete. Ready for human review in {self.run_dir}/4_emails.json")

if __name__ == "__main__":
    engine = OutboundEngine()
    engine.execute_pipeline()