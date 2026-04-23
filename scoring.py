def score_account(enriched, customers):
    score = 0

    for c in customers:

        # Industry match
        if c["industry"].lower() in enriched["industry"].lower():
            score += 40

        # Size similarity
        if abs(enriched["size"] - c["size"]) < 2000:
            score += 30

        # Geo match
        if c["geo"].lower() in enriched["geo"].lower():
            score += 30

    # normalize
    score = min(score, 100)

    if score > 75:
        tier = "Hot Fit"
    elif score > 45:
        tier = "Warm Fit"
    else:
        tier = "Low Fit"

    return {"score": score, "tier": tier}