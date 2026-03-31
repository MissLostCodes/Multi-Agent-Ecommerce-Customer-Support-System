# MultiAgent - E-Commerce AI Customer Support- 🤖🛍️

An AI-powered customer-service crew that ingests policy documents, classifies support tickets, and produces fully-cited, policy-compliant resolutions automatically.

 Fast ingest  Smart RAG  CrewAI  Gemini  Python313+

---

## Table of Contents

* [Why This Repo?](#why-this-repo)
* [Architecture](#architecture)
* [Project Structure](#project-structure)
* [Project Structure](#project-structure)
* [Outputs](#outputs)
* [Usage](#cli-usage)
* [Python API Usage](#python-api-usage)
* [Evaluation Suite](#evaluation-suite)
* [Extending Agents or Policies](#extending-agents-or-policies)
* [Contributing](#contributing)
* [Troubleshooting](#troubleshooting)
* [License](#license)


---

## Why This Repo?
Online stores face thousands of repetitive support requests.  
This repo automates **first-line responses**:
* Understands tickets via LLM triage
* Retrieves **only** relevant policy chunks
* Writes fully-cited replies or escalates intelligently
* 20 real-world test-cases baked in (≈ 85 % accuracy)

No GPUs needed—everything runs on Google's Gemini family (flash + embedding).

---

## Architecture
```
 flowchart LR
    A[Ticket] --> B[Triage Agent]
    B -->|classify| C{RAG Router}
    C -->|collection| D[ChromaDB]
    D --> E[Retriever Agent]
    E --> F[Writer Agent]
    F --> G[Compliance Agent]
    G --> H[Final Answer\nor ESCALATE]
```

1. **Triage Agent** (`crewai`) – classify ticket, detect missing info  
2. **Retriever Agent** – `Policy Search Tool` → exact Chroma collection (`refund`, `dispute`, `shipping`, …) via Gemini embedding-001  
3. **Writer Agent** – strict prompt: every claim must cite doc, else escalate  
4. **Compliance Agent** – reject hallucinations (citations < 1, fuzzy language)  

All results conform to `app.schemas.io.Output`.

---

## Project Structure
```
.
├── app/                       # Core source
│   ├── agents/                # CrewAI definitions
│   ├── core/                  # Gemini LLM wrapper
│   ├── graph/                 # Crew → workflow
│   ├── rag/                   # Embedding, ingestion, retrieval
│   ├── evaluation/            # Accuracy scoring
│   └── schemas/               # Pydantic models
├── data/
│   └── policies/              # Plaintext knowledge base
├── tests/
│   ├── test_cases.json        # 20 golden examples
│   └── test_e2e.py            # Pytest harness
├── ingestion_trigger.py       # One-click ingestion
└── pyproject.toml             # PEP-621 deps
```

---
## Outputs
![img.png](img.png)
![img_1.png](img_1.png)
![img_2.png](img_2.png)

---
## Installation

### Prerequisites
Python 3.13+  
Groq API key 
 

### uv (recommended)
```bash
uv init 
uv add -r requirements.txt
```

All dependencies listed in `pyproject.toml`.

---

## Usage
```bash
SET env variables 

# (1) Make sure Chroma is populated first
uv run ingestion_trigger.py

# (2) Run an interactive loop
uv run python -m app.main
     # default ticket in file
```
Change the hard-coded `ticket` string in `app/main.py` or:

```bash
python -c "
from app.main import workflow
print(workflow.run('Received damaged laptop – screen cracked, order #12345'))"
```

Sample output
```
{'classification':'refund',
 'confidence':0.93,
 'decision':'approve',
 'rationale':'Policy §Damaged Item allows refund/replace – evidence required...',
 'response':'We’re sorry... full refund processed.',
 'citations':['data/policies/disputes.txt', 'data/policies/returns_refunds.txt'],
 'notes':'APPROVED by compliance'}
```

---

## Python API Usage
```python
from app.main import workflow
payload = "Package lost, marked delivered but never arrived."

result = workflow.run(payload)
print(result.decision)   # → 'approve'
```

To re-use individual Crew agents (advanced):
```python
factory = AgentFactory(tools)
triage_agent  = factory.triage()
```

---

## Evaluation Suite
Evaluate on 20 curated tickets (accuracy, citation-score, escalation-rate):
```bash
pytest -q
```

Results summary printed per test-case from `tests/test_cases.json`.

---

## Extending Agents or Policies
1. Drop new `*.txt` files into `data/policies/`
2. Re-ingest: `python ingestion_trigger.py`
3. Add new classification in `RAGPipeline.get_collection()` mapping
4. Re-run tests: `pytest -q`  
5. (Opt.) tweak Crew prompts in `app/agents/crew_agents.py` for stricter leniency

---

## Contributing
We ❤️ pull requests.  
Please:
1. Fork & branch (`feature/`, `fix/`, `docs/`)
2. Add a unit or integration test (`tests/`)
3. Ensure `pytest` green
4. Update this README for user-facing changes
5. Submit PR with concise description

Code style = Black ≥ 24, isort, pep-8 naming.

---

## Troubleshooting
* `ValueError: GOOGLE_API_KEY not found` ➜ fill `.env`
* `chromadb.errors` on first run ➜ ensure you've run ingestion
* Reply too cautious (many escalations) ➜ lower `Compliance Agent` strictness or enrich policy docs
* Embeddings slow ➜ Gemini free tier limits; consider batching

---

## License
MIT – see LICENSE file. No warranties; commercial use at your own risk.