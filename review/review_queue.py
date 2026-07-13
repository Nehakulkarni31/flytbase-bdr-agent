import os
import json
import glob

def get_latest_run_dir() -> str | None:
    target_pattern = os.path.join("data", "run_*")
    run_dirs = glob.glob(target_pattern)
    if not run_dirs: return None
    return max(run_dirs, key=os.path.getmtime)

def run_review_queue():
    print("🔄 Booting up Human Review Gate...") 
    latest_dir = get_latest_run_dir()
    
    if not latest_dir:
        print("❌ Error: Could not find any run directories.")
        return

    emails_file = os.path.join(latest_dir, "4_emails.json")
    if not os.path.exists(emails_file):
        print(f"❌ Error: '{emails_file}' is missing.")
        return

    with open(emails_file, "r", encoding="utf-8") as f:
        drafts = json.load(f)

    print("=" * 70)
    print(f"📥 LOADING PLATFORM REVIEW QUEUE | RUN: {os.path.basename(latest_dir)}")
    print("=" * 70 + "\n")

    approved_list = []

    for idx, draft in enumerate(drafts):
        status = draft.get('verification_status', 'UNKNOWN').upper()
        
        print("=" * 70)
        print(f"📋 ACCOUNT COMPLIANCE DRILL-DOWN | DRAFT {idx + 1} OF {len(drafts)}")
        print(f"👤 Prospect: {draft.get('name', 'Unknown')} | {draft.get('title', 'Unknown Title')}")
        print(f"🏢 Enterprise Account: {draft.get('company_name', 'Unknown')}")
        print("-" * 70)
        
        # --- NEW VERIFICATION BLOCK ---
        if status == 'NEEDS_MANUAL_RESEARCH':
            print(f"⚠️  VERIFICATION: {status} - AI could not find a verifiable contact.")
        else:
            print(f"🔍 VERIFICATION: {status}")
            print(f"🔗 SOURCE URL: {draft.get('source_url', 'No URL captured')}")
        print("-" * 70)
        
        print(f"Subject: {draft.get('subject', 'No Subject')}")
        print(f"\nBody:\n{draft.get('draft_body', 'No Body Text Available')}")
        print("-" * 70)

        while True:
            choice = input("Action Required -> [A]pprove, [R]eject/Discard, [E]dit Copy: ").strip().lower()
            if choice == 'a':
                # Prevent blind approvals on unverified contacts
                if status == 'NEEDS_MANUAL_RESEARCH' and draft.get('name', '') in ['', 'Unknown', None]:
                    print("❌ Error: You cannot approve a draft without a Prospect Name. Select [E] to manually research and input a name.")
                    continue
                    
                draft['status'] = 'approved'
                approved_list.append(draft)
                print("✅ Copy Approved. Saved to batch queue.")
                break
            elif choice == 'r':
                print("❌ Copy Rejected. Discarded from pipeline.")
                break
            elif choice == 'e':
                print("\n[Entering Manual Revision Mode]")
                new_name = input(f"Prospect Name [{draft.get('name', '')}]: ") or draft.get('name', '')
                new_body = input("Type/Paste your edited email body text below:\n")
                
                draft['name'] = new_name
                draft['draft_body'] = new_body
                draft['status'] = 'approved_with_human_edits'
                approved_list.append(draft)
                print("📝 Revision Saved.")
                break
            else:
                print("Invalid operational command. Please select A, R, or E.")
        print("\n")

    output_payload_path = os.path.join(latest_dir, "final_approved_outreach.json")
    with open(output_payload_path, "w", encoding="utf-8") as f:
        json.dump(approved_list, f, indent=4)
        
    print(f"🎉 CAMPAIGN AUDIT COMPLETE | {len(approved_list)} EMAILS PASS COMPLIANCE")

if __name__ == "__main__":
    run_review_queue()