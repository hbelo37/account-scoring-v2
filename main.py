import json
from fastapi import FastAPI, HTTPException
from scoring import score_account
from enrich import enrich_company

app = FastAPI()

# In-memory ICP store (per server instance)
ICP_STORE = None


@app.post("/score")
def score_companies(payload: dict):
    """
    Payload formats supported:

    First time user (sets ICP + scores):
    {
        "companies": ["stripe.com"],
        "customers": [ ... ICP JSON ... ]
    }

    Next calls (only scoring):
    {
        "companies": ["notion.so"]
    }
    """

    global ICP_STORE

    companies = payload.get("companies")
    customers = payload.get("customers")

    # If customers provided → set ICP
    if customers:
        ICP_STORE = customers

    # If no ICP ever set → error
    if ICP_STORE is None:
        raise HTTPException(
            status_code=400,
            detail="ICP not set. Provide 'customers' in this request."
        )

    if not companies:
        raise HTTPException(
            status_code=400,
            detail="No companies provided to score."
        )

    results = []

    for company in companies:
        enriched = enrich_company(company)
        result = score_account(enriched, ICP_STORE)

        results.append({
            "company": company,
            "score": result["score"],
            "tier": result["tier"],
            "enriched": enriched
        })

    return {"results": results}