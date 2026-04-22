# 🚀 Account Scoring Skill (ICP-Driven)

A reusable GTM skill that lets any user:

1) Upload their existing customer dataset (ICP)
2) Score any company against that ICP using enrichment and scoring logic

This is designed to run as an API service and plug directly into tools like ChatGPT or Claude.

---

## 🧠 What this skill really does

Most scoring tools hardcode rules.

This skill does something smarter:

You bring your customer data.
The engine learns your ICP.
Then it scores any company against it.

This makes it a true reusable GTM Account Scoring Engine.

---

## ⚙️ How it works

Step 1 — User uploads their customers once  
Step 2 — User asks to score companies anytime after  

The system enriches the company, compares it with the uploaded ICP, and returns a score and tier.

---

## 📦 Project Structure

main.py → FastAPI app with endpoints  
enrich.py → Company enrichment logic (Smarte, Crunchbase, ZoomInfo, etc.)  
scoring.py → ICP comparison and py → Helper utilities if needed  
cli.py → Local CLI testing  
requirements.txt → Dependencies  

---

## 🔌 API Endpoints

### POST /set-icp

Upload customer dataset.

Body should contain a list named customers with firmographic data like company, industry, size, geo.

Response: ICP stored successfully.

---

### POST /score

Score companies against the uploaded ICP.

Body should contain a list named companies with company names or domains.

Response: company name, score, tier, enriched firmographic data.

---

## ▶️ Run locally

Install dependencies:

pip install -r requirements.txt

Run server:

uvicorn main:app --reload

Open:

http://127.0.0.1:8000/docs

Test the endpoints from Swagger.

---

## ☁️ Deploy on Render

Create a Web Service from this repo.

Build command:
pip install -r requirements.txt

Start command:
uvicorn main:app --host 0.0.0.0 --port 10000

Add environment variable:

SMARTE_API_KEY with your enrichment key.

After deploy, open /docs to test.

---

## 🧮 Himportant)

All scoring logic lives in scoring.py.

This function is the only thing that matters:

score_account(account, icp_data)

As long as this function:
- takes enriched company data
- takes ICP dataset
- returns score and tier

Everything else will continue working.

---

## ✏️ Changing scoring logic

You can change scoring to:

- Rule based weights
- Industry match percentage
- Size similarity
- Geo similarity
- Tech stack overlap
- Funding stage similarity
- Or full similarity algorithms

Only edit scoring.py. Nothing else.

---

## 🔄 Changing enrichment provider

All enrichment is isolated in enrich.py.

You can swap Smarte with Crunchbase, ZoomInfo, Clearbit, Apollo, or any provider.

As long as enrich_company returns a standard firmographic dictionary, scoring continues to work.

---

## 🤖 Using this as a Skill in ChatGPT or Claude

Tool flow:

1) Tool calls /set-icp with user customers
2) Tool calls /score whenever user asks to score companies

This makes the skill reusable for anyone## 🧩 Why this is powerful

This is not a demo script.
This is a real ICP scoring engine that adapts to whoever uses it.

Bring your customers.
Score your market.

