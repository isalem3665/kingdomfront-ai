"""
Reflection Agent v0
Reads feedback.csv and updates item popularity weights.
"""

import pandas as pd, json, os

DATA_PATH = os.getenv("DATA_PATH", "data/events_riyadh.csv")
FEEDBACK_PATH = "data/feedback.csv"
OUTPUT_PATH = "data/events_reflected.csv"

def reflect():
    df = pd.read_csv(DATA_PATH)
    if not os.path.exists(FEEDBACK_PATH):
        print("No feedback yet.")
        return
    fb = pd.read_csv(FEEDBACK_PATH)
    summary = fb.groupby("item_id")["rating"].mean().reset_index()
    df = df.merge(summary, on="id", how="left")
    df["adjusted_score"] = df["rating_y"].fillna(0) * 0.5 + df.get("rating_x", 3) * 0.5
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Reflection complete. Updated file → {OUTPUT_PATH}")

if __name__ == "__main__":
    reflect()
