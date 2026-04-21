ICP = {}

def train_icp(customers: list):
    global ICP
    ICP = {
        "industry": [c["industry"] for c in customers],
        "geo": [c["geo"] for c in customers],
        "funding": [c["funding_stage"] for c in customers],
        "avg_size": sum(c["size"] for c in customers) / len(customers),
        "avg_revenue": sum(c["revenue"] for c in customers) / len(customers),
        "tech": set(t for c in customers for t in c.get("tech_stack", [])),
    }

def get_icp():
    if not ICP:
        raise Exception("ICP not trained")
    return ICP