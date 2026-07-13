# Autonomous BDR Agent – FlytBase Pipeline

An AI-assisted outbound prospecting pipeline built for the FlytBase Outbound BDR – AI-Native Hunter assignment.

The system automates the early stages of enterprise outbound sales by programmatically identifying targets, discovering decision-makers, synthesizing live market research, and drafting highly personalized outreach. To guarantee brand safety, it routes all drafts through a strict, terminal-based **Human-in-the-Loop (HITL) review queue** before any email is cleared for production.

Instead of deploying a basic, fragile LLM wrapper, this system is engineered around **accuracy, fault-tolerant modularity, and explicit state preservation**.

---

## 🏗️ Project Structure

```text
flytbase-outbound-agent/
│
├── config/
│   └── campaign_brief.yaml      # Target ICP, roles, and core product angles
│
├── agents/
│   ├── account_finder.py        # Identifies target enterprise companies
│   ├── contact_finder.py        # Discovers key decision-makers via strict rules
│   ├── research_synthesizer.py  # Gathers live web signals and market news
│   └── email_generator.py       # Contextually drafts personalized copy
│
├── tools/
│   ├── web_search.py            # Custom search wrappers and parsing utilities
│   └── llm_client.py            # Centralized API inference client
│
├── review/
│   └── review_queue.py          # Interactive HITL terminal review engine
│
├── data/                        # Persistent state storage (Git-ignored)
│   └── run_<timestamp>/
│       ├── accounts.json
│       ├── contacts.json
│       ├── research.json
│       └── emails.json
│
├── logs/                        # Detailed runtime execution tracing
│   └── run_<timestamp>.log
│
├── tests/
│   └── test_pipeline.py         # Standard pipeline testing suites
│
├── orchestrator.py              # Main execution controller
├── requirements.txt             # Project dependencies
├── .env.example                 # Template for required API keys
└── README.md                    # System documentation
```

## 🔄 Pipeline Flow

```text
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
[ Human Review Queue ] ◄── (Validates Contacts, Catches Broken/Generic Drafts)
        │
        ▼
[ Approved Outreach JSON ]
```

---

## ⚡ Key Features

1. **Modular Agent Architecture** — Responsibilities are fully decoupled across isolated scripts, making the system maintainable and easily extensible.
2. **Idempotent State Management** — The pipeline serializes structured JSON payloads at every discrete stage. If a downstream network call or API limit fails midway, the state is preserved and execution resumes without losing upstream scraped data.
3. **Anti-Hallucination Gating** — The contact discovery agent operates under strict validation rules. If a currently-serving executive with an accompanying source URL cannot be confidently resolved, it falls back to a visible `NEEDS_MANUAL_RESEARCH` flag instead of letting the LLM guess silently from internal/outdated knowledge.
4. **Live Signals Synthesis** — Pulls real-time company events, press releases, and expansion signals to create contextual hooks rather than generic marketing templates.

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/flytbase-outbound-agent.git
cd flytbase-outbound-agent
```

### 2. Configure a Virtual Environment

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a file named exactly `.env` in the project root, using `.env.example` as a template:

```bash
GROQ_API_KEY=your_actual_api_key_here

# Supporting options depending on configuration:
# OPENAI_API_KEY=your_key_here
# ANTHROPIC_API_KEY=your_key_here
```

> ⚠️ **Security Warning:** The `.env` file contains production credentials and is explicitly blocked via `.gitignore` to ensure no secrets leak to public repositories.

---

## 🚀 Running the Project

The pipeline executes in two distinct stages to ensure deterministic control.

### Stage 1 — Discovery & Copy Generation

```bash
python orchestrator.py
```

What the orchestrator executes:

- Parses `config/campaign_brief.yaml` to extract targeted parameters (e.g., Latin American lithium, copper, and iron ore extraction operations like SQM, Codelco, and Vale).
- Maps target accounts and looks up high-leverage roles (e.g., Head of Operations, VP of HSE, Site Director).
- Searches live news indices for account-specific trigger signals (e.g., CapEx expansions, safety mandates).
- Structures localized drafts connecting FlytBase's autonomous 24/7 drone platform directly to those site hazards.
- Saves individual stage logs and outputs to a uniquely tracked folder inside `data/run_<timestamp>/`.

### Stage 2 — Interactive Human Review Queue

```bash
python review/review_queue.py
```

The terminal launches an interactive CLI, serving drafts sequentially. Reviewers step through entries using three core actions:

- **A — Approve:** Moves the draft to the final output file. Use when the contact identity is fully accurate, source URLs are verified, and the personalization hook cleanly matches the FlytBase positioning.
- **R — Reject:** Discards the draft entirely. Use if the target persona is out of date, the company falls outside the target parameters, or data points appear unverified.
- **E — Edit:** Safe override. Use if the copy is strategically sound but contains generic AI phrasing, minor name formatting issues, or needs a stronger call-to-action. The CLI prompts for corrections directly, updating the payload before moving to the next item.

---

## 📂 Final Output Delivery

Once all queued entries are processed, sanitized outputs are flattened and written to:

```text
data/final_approved_outreach.json
```

This structured output can be imported as a clean JSON/CSV payload into active B2B sequencing tools, including Apollo, HubSpot, Outreach, or Salesloft.

---

## 🧪 Testing

```bash
python tests/test_pipeline.py
```

---

## 🛠️ Engineering Decisions & Trade-offs

- **Human-Gated Execution** — AI is never permitted to run unmonitored outreach. The CLI gate ensures compliance with brand standards and message quality before anything is send-ready.
- **Visible Failures Over Silent Guessing** — The anti-hallucination constraint handles unverified web snippets by appending a `NEEDS_MANUAL_RESEARCH` status, forcing visible human intervention rather than allowing an unverifiable name to slip through as fact.
- **State Decoupling** — Independent intermediate JSON stages create architectural modularity, so individual layers can be modified, updated, or debugged without refactoring the entire sequence.

---

## 📈 Future Scalability Improvements

Given a higher tool budget or extended timeline:

- **Enrichment Key Upgrades** — Swap the free search scrapers for dedicated integrations (Apollo API, LinkedIn Sales Navigator) to raise contact hit rates.
- **Concurrent Processing** — Refactor with Python `asyncio` to process hundreds of target accounts in parallel rather than sequentially.
- **UI Enhancements** — Move the terminal review interface into a lightweight Streamlit dashboard for a faster reviewer workflow.
- **Confidence Scoring** — Introduce a scoring layer to flag lower-confidence generations for closer review before they even reach the human gate.

---

## 🧑‍💻 Author

**Neha Girish Kulkarni** — B.E. Computer Engineering (Final Year)

Developed for the FlytBase Outbound BDR – AI-Native Hunter assessment.
