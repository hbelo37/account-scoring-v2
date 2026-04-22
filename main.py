from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from enrich import enrich_company
from scoring import score_account

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
    global ICP_STORE

    if not payload.customers:
        raise HTTPException(status_code=400, detail="Customers list cannot be empty")

    ICP_STORE = payload.customers

    return {
        "message": "ICP stored successfully",
        "customers_loaded": len(ICP_STORE)
    }


@app.post("/score")
def score_companies(payload: ScorePayload):
    if not ICP_STORE:
        raise HTTPException(
            status_code=400,
            detail="ICP not set. Call /set-icp first with customer data."
        )

    results = []

    for company in payload.companies:
        enriched = enrich_company(company)

        # scoring.py should use ICP_STORE internally
        result = score_account(enriched, ICP_STORE)

        results.append({
            "company": company,
            "score": result["score"],
            "tier": result["tier"],
            "enriched": enriched
        })

    return {"results": results}