import requests
import re

SMARTE_ENRICH_URL = "https://api.smarte.pro/v7/enrich"
API_KEY = "7aca4a79-f88f-44d4-bd63-d99bbe2d6bb7"

def parse_rev_range(rev_range: str) -> float:
    """Convert revenue range string like '$100 - 250M' to a number (midpoint)."""
    if not rev_range:
        return 0
    # find numbers
    parts = re.findall(r'\$?([\d\.]+)([KMB]?)', rev_range)
    if not parts:
        return 0
    vals = []
    for num, suffix in parts:
        n = float(num)
        if suffix == "K":
            n *= 1e3
        elif suffix == "M":
            n *= 1e6
        elif suffix == "B":
            n *= 1e9
        vals.append(n)
    return sum(vals) / len(vals) if vals else 0

def enrich_company(name_or_domain: str):
    """Call SMARTe Enrich API to get firmographics for a company."""
    headers = {
        "apikey": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "companyName": name_or_domain,
        "companyWebAddress": name_or_domain
    }

    resp = requests.post(SMARTE_ENRICH_URL, json=payload, headers=headers)
    data = resp.json()

    # Map response to scoring format
    account = {
        "company": data.get("compName") or name_or_domain,
        "industry": data.get("compIndustry") or "Unknown",
        "size": int(data.get("compEmpCount") or 0),
        "revenue": parse_rev_range(data.get("compRevRange") or ""),
        "geo": data.get("compCountry") or "Unknown",
        "tech_stack": [],          # SMARTe doesn’t return tech stack here
        "funding_stage": None      # Would require another API or mapping
    }

    return account