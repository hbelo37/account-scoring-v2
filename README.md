# 🚀 Account Scoring Skill — Bring Your Own Enrichment API

A portable **ICP-aware account scoring engine** that works with **any enrichment data provider**.

Plug in:
- SMARTe
- Crunchbase
- ZoomInfo
- LeadIQ
- Or your internal data API

Without changing the scoring logic.

---

## 🧠 Core Idea

Most account scoring tools use static rules.

This skill scores companies based on:

> “How similar is this company to the ones who already pay us?”

Your **existing customers** define the ICP.  
Any new company is enriched via **your chosen provider** and scored against that ICP memory.

---

## 🧱 Architecture

User Input (company/domain)  
→ enrich.py → Your Provider API  
→ Standardized Firmographic Schema  
→ scoring.py (ICP comparison logic)  
→ Score + Tier

---

## 📁 Project Structure

account_scoring_skill/

- cli.py — User entry point
- enrich.py — Chooses provider
- provider_base.py — Provider interface
- provider_smarte.py — Example provideic (never changes)
- customers.json — Your real customer dataset
- .env — API keys
- requirements.txt

---

## 🔌 Bring Your Own Provider

Every provider only needs to return this **standard schema**:

{
  "company": str,
  "industry": str,
  "size": int,
  "revenue": float,
  "geo": str,
  "tech_stack": list,
  "funding_stage": str | None
}

As long as this schema is returned → scoring works.

---

## ✏️ Adding a New Provider (Example)

Create `provider_crunchbase.py`:

from provider_base import EnrichmentProvider

class CrunchbaseProvider(EnrichmentProvider):
    def enrich(self, query: str) -> dict:
        # call Crunchbase API
        return { standardized schema }

Then change one line in `enrich.py`:

from provider_crunchbase import CrunchbaseProvider as Provider

Done. No scoring changes needed.

---

## 🧠 ICP Memory — customers.json

This file defines your Ideal Customer Profile.

Add your real customers here:

[
  {
    "company": "Acme SaaS",
    "industry": "SaaS",
    "size": 200,
  0000,
    "geo": "US",
    "tech_stack": ["aws", "salesforce"],
    "funding_stage": "Series B"
  }
]

The richer this file → the smarter the scoring.

---

## ▶️ Run Locally

python -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt  

Create `.env`:

SMARTE_API_KEY=your_key_here

Run:

python cli.py

Input example:

stripe.com

Output example:

{'score': 91, 'tier': 'High Fit'}

---

## 🧩 Why This Is Powerful

This is not a scoring script.

This is a **GTM skill** you can expose to:
- ChatGPT tools
- Claude tools
- MCP servers
- Internal sales workflows

Because enrichment and scoring are fully decoupled.

---

## 🛣️ Roadmap

- FastAPI wrapper for tool usage
- Batch scoring via CSV
- Vector similarity vs rule scoring
- Technographic matching
- Revenue range parsing

---

## 🪪 License

MIT
