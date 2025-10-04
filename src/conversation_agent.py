"""
Conversation Agent
Extracts user intent and structured context (city, time, budget, category)
using an LLM prompt + JSON output format.
"""
from dotenv import load_dotenv
load_dotenv()

import json, os
from openai import OpenAI

MODEL = os.getenv("MODEL_NAME", "gpt-4o-mini")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

INTENT_PROMPT = """
You are a travel assistant for Saudi users.
Given a message, extract:
- intent (e.g., find_activity, book_event, ask_weather)
- city
- time (today, tonight, weekend)
- budget_sar (integer if mentioned)
- category (restaurant, outdoor, family, culture, shopping, general)
Return strict JSON only.
"""

def extract_intent(message: str) -> dict:
    prompt = f"{INTENT_PROMPT}\n\nUser: {message}"
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.2,
    )
    try:
        data = json.loads(resp.choices[0].message.content)
    except Exception:
        data = {"intent": "unknown", "city": None, "category": None}
    return data

if __name__ == "__main__":
    msg = input("Ask: ")
    print(extract_intent(msg))
