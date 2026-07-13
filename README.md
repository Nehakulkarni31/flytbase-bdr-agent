Autonomous BDR Agent – FlytBase Pipeline
An AI-assisted outbound prospecting pipeline built for the FlytBase AI-Native BDR role assignment.

The system automates the early stages of enterprise outbound sales by programmatically identifying targets, discovering decision-makers, synthesizing live market research, and drafting highly personalized outreach. To guarantee brand safety, it routes all drafts through a strict, terminal-based Human-in-the-Loop (HITL) review queue before any email is cleared for production.

Instead of deploying a basic, fragile LLM wrapper, this system is engineered around accuracy, fault-tolerant modularity, and explicit state preservation.

🏗️ Project Structure
Plaintext
flytbase-outbound-agent/
│
├── config/
│ └── campaign*brief.yaml # Target ICP, roles, and core product angles
│
├── agents/
│ ├── account_finder.py # Identifies target enterprise companies
│ ├── contact_finder.py # Discovers key decision-makers via strict rules
│ ├── research_synthesizer.py # Gathers live web signals and market news
│ └── email_generator.py # Contextually drafts personalized copy
│
├── tools/
│ ├── web_search.py # Custom search wrappers and parsing utilities
│ └── llm_client.py # Centralized API inference client
│
├── review/
│ └── review_queue.py # Interactive HITL terminal review engine
│
├── data/ # Persistent state storage (Git-ignored)
│ └── run*<timestamp>/
│ ├── accounts.json
│ ├── contacts.json
│ ├── research.json
│ └── emails.json
│
├── logs/ # Detailed runtime execution tracing
│ └── run\_<timestamp>.log
│
├── tests/
│ └── test_pipeline.py # Standard pipeline testing suites
│
├── orchestrator.py # Main execution controller
├── requirements.txt # Project dependencies
├── .env.example # Template for required API keys
└── README.md # System documentation
🔄 Pipeline Flow
Plaintext
[ Campaign Brief ]
│
▼
[ Account Finder ]
│
▼
[ Contact Finder ]
│
▼
[ Company Research ]
│
▼
[ Email Generator ]
│
▼
[ Human Review Queue ] ◄── (Stops AI Drift / Validates Contacts)
│
▼
[ Approved Outreach JSON ]
⚡ Key Features
Modular Agent Architecture: Responsibilities are fully decoupled across isolated tracking scripts, making the system maintainable and easily extensible.

Idempotent State Management: The pipeline serializes and saves structural JSON payloads at every discrete stage. If a downstream network call or API limit fails midway, the state is preserved and execution resumes seamlessly without losing upstream scraped data.

Anti-Hallucination Gating: The contact discovery agent operates under strict validation rules. If a highly verified current executive with an accompanying source URL cannot be confidently resolved, it falls back to a visible NEEDS_MANUAL_RESEARCH flag instead of letting the LLM guess silently.

Live Signals Synthesis: Pulls real-time company events, press releases, and scaling indices to create contextual hooks rather than generic marketing templates.

⚙️ Installation & Setup

1. Clone the Repository
   Bash
   git clone https://github.com/<your-username>/flytbase-outbound-agent.git
   cd flytbase-outbound-agent
2. Configure a Virtual Environment
   Windows:

Bash
python -m venv .venv
.venv\Scripts\activate
macOS / Linux:

Bash
python3 -m venv .venv
source .venv/bin/activate 3. Install Dependencies
Bash
pip install -r requirements.txt 4. Configure Environment Variables
Create a localized environment file in the root directory named exactly .env using the template format found in .env.example:

Code snippet
GROQ_API_KEY=your_actual_api_key_here

# Supporting options depending on configuration:

# OPENAI_API_KEY=your_key_here

# ANTHROPIC_API_KEY=your_key_here

⚠️ Security Warning: The .env file contains production credentials and is explicitly blocked via the .gitignore configuration to ensure no secrets leak to public repositories.

🚀 Running the Project
The pipeline executes in two distinct stages to ensure deterministic control.

Stage 1 — Discovery & Copy Generation
Run the core background pipeline to process the targeted accounts:

Bash
python orchestrator.py
What the Orchestrator executes:

Parses config/campaign_brief.yaml to extract targeted parameters (e.g., Latin American lithium, copper, and iron ore extraction operations like SQM, Codelco, and Vale).

Maps target accounts and looks up high-leverage roles (e.g., Head of Operations, VP of HSE, Site Director).

Searches live news indices for account-specific trigger signals (e.g., CapEx expansions, safety mandates).

Structures localized drafts connecting FlytBase’s autonomous 24/7 drone platform directly to those site hazards.

Saves individual stage logs and outputs to a uniquely tracked folder inside data/run\_<timestamp>/.

Stage 2 — Interactive Human Review Queue
Once the generation steps finish, execute the human-in-the-loop review mechanism to audit the output:

Bash
python review/review_queue.py
The terminal launches an interactive command-line interface, serving drafts sequentially. Reviewers step through entries manually using three core control actions:

A — Approve: Moves the draft to the final output file. Use this when the contact identity is fully accurate, URLs are verified, and the personalization hook cleanly matches the FlytBase positioning.

R — Reject: Completely discards the draft. Use this if the target persona is out of date, the company falls outside the exact target parameters, or data points appear unverified.

E — Edit: Safe override command. Use this if the copy is strategically sound but contains generic AI text layouts, minor name formatting issues, or requires a stronger call-to-action. The application prompts you to provide corrections directly in the terminal, updating the payload instantly before moving to the next item.

📂 Final Output Delivery
When all generated queue entries are processed via the review script, the sanitized outputs are flattened and written to:

Plaintext
data/final_approved_outreach.json
This final, structured document represents highly reliable prospecting data and can be instantly imported as a clean CSV/JSON payload into active B2B sequencing suites, including:

Apollo

HubSpot

Outreach

Salesloft

🧪 Testing
To evaluate pipeline behaviors and run configuration checks across the internal systems, execute:

Bash
python tests/test_pipeline.py
🛠️ Engineering Decisions & Trade-offs
Human Gated Execution: AI is completely prohibited from running unmonitored outreach channels. The CLI gate ensures total compliance with brand standards and target message quality.

Visible Failures Over Silent Guessing: The anti-hallucination constraint handles unverified web snippets by intentionally appending a NEEDS_MANUAL_RESEARCH status tag, forcing visible human intervention rather than allowing false assumptions to slip through.

State Decoupling: Writing independent intermediate JSON stages creates architectural modularity, allowing individual layers to be modified, updated, or debugged without needing to refactor the entire sequence.

📈 Future Scalability Improvements
If granted a higher tool budget or extended timeline, the architecture would be optimized as follows:

Enrichment Key Upgrades: Swapping the underlying free search scrapers out for dedicated enterprise integrations (e.g., direct Apollo API or LinkedIn Sales Navigator API data keys) to maximize baseline profile hit rates.

Concurrent Threading: Refactoring execution blocks with Python asyncio patterns to safely process hundreds of enterprise target profiles in parallel rather than sequentially.

UI Enhancements: Transitioning the terminal-based interface into a lightweight, dashboard-driven Streamlit or Flask application for optimized human review workflows.

Telemetry Analysis: Introducing confidence scoring models and algorithmic text evaluations to measure and optimize semantic drift across generation windows.

🧑‍💻 Author
Neha Kulkarni – Third-Year Computer Engineering Student

Developed for the FlytBase AI-Native BDR Assessment.
