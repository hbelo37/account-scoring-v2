from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from enrich import enrich_company
from scoring import score_account

app = FastAPI()


class CustomerExample(BaseModel):
    industry: str
    size: int
    geo: str


class ScorePayload(BaseModel):
    companies: List[str]
    customers: List[CustomerExample]


@app.post("/score")
def score_companies(payload: ScorePayload):
    results = []

    for company in payload.companies:
        enriched = enrich_company(company)

        result = score_account(
            enriched,
            [c.dict() for c in payload.customers]
        )

        results.append({
            "company": company,
            "score": result["score"],
            "tier": result["tier"],
            "enriched": enriched
        })

    return {"results": results}