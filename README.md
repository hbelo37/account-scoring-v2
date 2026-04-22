# 🚀 Account Scoring Skill — Bring Your Own Enrichment API

A portable, ICP-aware **Account Scoring Engine** that works with **any enrichment data provider**.

Use SMARTe, Crunchbase, ZoomInfo, LeadIQ, or your own internal API —  
without changing the scoring system.

---

## 🧠 Core Idea

Most tools score accounts using static firmographic rules.

This skill scores accounts based on:

“How similar is this company to the ones who already pay us?”

Your existing customers define the ICP.  
Any new company is enriched using your chosen provider and scored against that ICP memory.

---

## 🧱 Architecture

User Input (company/domain)  
→ enrich.py → Your Provider API  
→ Standardized Firmographic Schema  
→ scoring.py (ICP logic)  
→ Score + Tier

---

## 📁 Project Structure

- cli.py — User entry point
- enrich.py — Chooses provider
- provider_base.py — Provider interface
- provider_smarte.py — Example provider
- scoring.py — Scoring logic (isolated)
- customers.json — Your ICP dataset
- .env — API keys
- requirements.txt

---

## 🔌 Bring Your Own Provider

Every provider only needs to return this standard schema:

{
  "company": str,
  "industry": str,
  "size": int,
  "revenue": float,
  "geo": str,
  "tech_stack": list,
  "funding_stage": str | None
}

As long as this is returned, scoring works.

To add a new provider:

1. Create provider_xxx.py implementing enrich()
2. Return the standardized schema
3. Change one line in enrich.py to use that provider

No scoring changes required.

---

## 🧠 ICP Memory — customers.json

This file defines your Ideal Customer Profile.

Example:

[
  {
    "company": "Acme SaaS",
    "industry": "SaaS",
    "size": 200,
    "revenue": 5000000,
    "geo": "US",
    "tech_stack": ["aws", "salesforce"],
    "funding_stage": "Series B"
  }
]

The richer this file, the smarter the scoring.

---

## 🧮 How to Change the Scoring Logic (Very Important)

All scoring lives in **scoring.py**.

You can change scoring without touching:
- providers
- enrichment
- CLI
- future API wrappers

### Required function

def score_account(account: dict) -> dict:

Input will look like:

{
  "company": "...",
  "industry": "...",
  "size": ...,
  "revenue": ...,
  "geo": "...",
  "tech_stack": [...],
  "funding_stage": ...
}

Output must be:

{"score": int, "tier": "High Fit" | "Medium Fit" | "Low Fit"}

---

### Example 1 — Rule Based Scoring

def score_account(account: dict) -> dict:
    score = 0

    if account["industry"] in ["SaaS", "Software", "Sales intelligence"]:
        score += 40

    if 100 <= account["size"] <= 2000:
        score += 30

    if account["geo"] in ["United States", "US", "USA"]:
        score += 20

    if account.get("funding_stage") in ["Series A", "Series B"]:
        score += 20

    if score >= 70:
        tier = "High Fit"
    elif score >= 40:
        tier = "Medium Fit"
    else:
        tier = "Low Fit"

    return {"score": score, "tier": tier}

---

### Example 2 — ICP Similarity Scoring (Recommended)

import json

with open("customers.json") as f:
    customers = json.load(f)

def score_account(account: dict) -> dict:
    score = 0

    industries = [c["industry"] for c in customers]
    sizes = [c["size"] for c in customers]
    geos = [c["geo"] for c in customers]

    if account["industry"] in industries:
        score += 35

    if min(sizes) <= account["size"] <= max(sizes):
        score += 30

    if account["geo"] in geos:
        score += 20

    if score >= 70:
        tier = "High Fit"
    elif score >= 40:
        tier = "Medium Fit"
    else:
        tier = "Low Fit"

    return {"score": score, "tier": tier}

---

## ▶️ Run Locally

python -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt  

Create .env with your API key.

Run:

python cli.py

---

## 🧩 Why This Is Powerful

This is a GTM skill you can expose to:
- ChatGPT tools
- Claude tools
- MCP servers
- Internal workflows

Because enrichment and scoring are fully decoupled.

---

## License

MIT
"""
open("README.md","w").write(content)
PY

git add README.md
git commit -m "Full rewritten README"
git push
