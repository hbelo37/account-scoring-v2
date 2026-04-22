from fastapi import FastAPI
from pydantic import BaseModel

from enrich import enrich_company
from scoring import score_account

app = FastAPI()


class AccountRequest(BaseModel):
    company: str


@app.post("/score")
def score(req: AccountRequest):
    account = enrich_company(req.company)
    result = score_account(account)
    return {
        "input": req.company,
        "enriched": account,
        "result": result
    }