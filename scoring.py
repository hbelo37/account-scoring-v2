from collections import Counter
import statistics


def build_icp_profile(customers):
    industries = [c["industry"] for c in customers]
    geos = [c["geo"] for c in customers]
    sizes = [c["size"] for c in customers]

    return {
        "top_industries": Counter(industries),
        "top_geos": Counter(geos),
        "avg_size": statistics.mean(sizes),
    }


def score_account(enriched, customers):
    icp = build_icp_profile(customers)

    score = 0

    # Industry similarity (0-40)
    if enriched["industry"] in icp["top_industries"]:
        freq = icp["top_industries"][enriched["industry"]]
        score += min(40, freq * 10)

    # Geo similarity (0-20)
    if enriched["geo"] in icp["top_geos"]:
        freq = icp["top_geos"][enriched["geo"]]
        score += min(20, freq * 5)

    # Size similarity (0-40)
    size_diff = abs(enriched["size"] - icp["avg_size"])
    size_score = max(0, 40 - (size_diff / icp["avg_size"]) * 40)
    score += size_score

    # Tiering
    if score >= 70:
        tier = "High Fit"
    elif score >= 40:
        tier = "Medium Fit"
    else:
        tier = "Low Fit"

    return {
        "score": round(score),
        "tier": tier
    }