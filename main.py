from fastapi import FastAPI
from icp import train_icp
from scoring import score

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/train_icp")
def train(data: dict):
    train_icp(data["customers"])
    return {"message": "trained"}

@app.post("/score")
def run_score(data: dict):
    return score(data["account"])