from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from enrich import enrich_company
from scoring import score_account
import json
import os

ICP_FILE = "icp_store.json"

app = FastAPI(title="Account Scoring Skill")

# In-memory ICP store (per service instance)
ICP_STORE: List[Dict] = []


# ---------- Models ----------

class ICPPayload(BaseModel):
    customers: List[Dict]


class ScorePayload(BaseModel):
    companies: List[str]  # names or domains


# ---------- Routes ----------

@app.get("/")
def health():
    return {"status": "Account Scoring Skill running"}


@app.post("/set-icp")
def set_icp(payload: ICPPayload):
    import json

    ICP_FILE = "icp_store.json"

    if not payload.customers:
        raise HTTPException(status_code=400, detail="Customers list cannot be empty")

    with open(ICP_FILE, "w") as f:
        json.dump(payload.customers, f)

    return {
        "message": "ICP stored successfully",
        "customers_loaded": len(payload.customers)
    }

@app.post("/score")
def score_companies(payload: ScorePayload):
    import os
    import json

    ICP_FILE = "icp_store.json"

    # Check if ICP exists
    if not os.path.exists(ICP_FILE):
        raise HTTPException(
            status_code=400,
            detail="ICP not set. Call /set-icp first with customer data."
        )

    # Load ICP from file
    with open(ICP_FILE, "r") as f:
        icp_data = json.load(f)

    results = []

    for company in payload.companies:
        enriched = enrich_company(company)

        result = score_account(enriched, icp_data)

        results.append({
            "company": company,
            "score": result["score"],
            "tier": result["tier"],
            "enriched": enriched
        })

    return {"results": results}