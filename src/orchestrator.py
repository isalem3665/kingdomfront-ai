"""
Cognitive Orchestrator v0
Chains Conversation → Recommendation → Response JSON
"""

import argparse, json, time
from conversation_agent import extract_intent
from recommendation_agent import recommend

def run_pipeline(query: str):
    t0 = time.time()
    intent = extract_intent(query)
    context = {
        "city": intent.get("city"),
        "category": intent.get("category"),
        "budget": intent.get("budget_sar"),
        "time": intent.get("time"),
    }
    recs = recommend(context)
    t1 = time.time()
    result = {
        "intent": intent.get("intent"),
        "context": context,
        "recommendations": recs,
        "latency_sec": round(t1 - t0, 2),
    }
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, required=True, help="User question")
    args = parser.parse_args()

    output = run_pipeline(args.query)
    print(json.dumps(output, indent=2, ensure_ascii=False))
