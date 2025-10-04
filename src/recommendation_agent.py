"""
Recommendation Agent
Simple hybrid: keyword/tag match + LLM reranker.
"""

import os, json, pandas as pd
from openai import OpenAI

MODEL = os.getenv("MODEL_NAME", "gpt-4o-mini")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DATA_PATH = os.getenv("DATA_PATH", "data/events_riyadh.csv")

def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    return df.fillna("")

def search_candidates(df, category=None, city=None):
    if category:
        df = df[df["category"].str.contains(category, case=False, na=False)]
    if city:
        df = df[df["city"].str.contains(city, case=False, na=False)]
    return df.sample(min(len(df), 10)).to_dict("records")

def rerank(context: dict, candidates: list) -> list:
    items = "\n".join(
        [f"- {c['title']} ({c.get('category','')}, {c.get('price_sar','?')} SAR)" for c in candidates]
    )
    prompt = f"""
You are ranking Riyadh activities for a user.
User context: {json.dumps(context)}
Candidates:\n{items}
Return top 5 as JSON list with fields [title, reason, score 0–1].
"""
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.4,
    )
    try:
        ranked = json.loads(resp.choices[0].message.content)
    except Exception:
        ranked = [{"title": c["title"], "reason": "default", "score": 0.5} for c in candidates[:5]]
    return ranked

def recommend(context: dict):
    df = load_data()
    cands = search_candidates(df, context.get("category"), context.get("city"))
    return rerank(context, cands)

if __name__ == "__main__":
    ctx = {"city": "Riyadh", "budget": 200, "category": "family", "time": "tonight"}
    print(json.dumps(recommend(ctx), indent=2, ensure_ascii=False))
