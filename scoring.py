from icp import get_icp

def score_account(account: dict, icp_data: list) -> dict:
    score = 0

    # Industry fit
    if account["industry"] in ["SaaS", "Sales intelligence", "Software"]:
        score += 30

    # Company size
    if 50 <= account["size"] <= 1000:
        score += 25

    # Geo fit
    if account["geo"] in ["United States", "US", "USA"]:
        score += 15

    # Basic revenue logic (optional)
    if account.get("revenue", 0) > 1_000_000:
        score += 10

    # Simple tiering
    if score >= 70:
        tier = "High Fit"
    elif score >= 40:
        tier = "Medium Fit"
    else:
        tier = "Low Fit"

    return {"score": score, "tier": tier}