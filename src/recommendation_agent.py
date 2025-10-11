"""
Recommendation Agent (Final Version)
Combines strict CSV logic + normalization + reflection bias + fallback.
"""

import json
import pandas as pd
from pathlib import Path
from typing import Dict

# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------
DATA_PATH = Path("data/events_riyadh_clean.csv")   # cleaned CSV file
REFLECTION_MEMORY = Path("data/reflection_memory.json")

# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------
def load_data() -> pd.DataFrame:
    """Load the base CSV dataset safely."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"❌ Dataset not found: {DATA_PATH}")
    # tolerate any remaining bad rows
    df = pd.read_csv(DATA_PATH, on_bad_lines="skip").fillna("")
    return df


def _load_reflection_preferences() -> Dict[str, float]:
    """Load user preference scores from reflection memory (if exists)."""
    if not REFLECTION_MEMORY.exists():
        return {}
    try:
        with open(REFLECTION_MEMORY, "r", encoding="utf-8") as f:
            memory = json.load(f)
        prefs = {}
        for i in memory.get("interactions", []):
            fb = i.get("feedback")
            for item in i.get("response", []):
                title = item.get("title")
                if title:
                    prefs[title] = prefs.get(title, 0) + (1 if fb == "positive" else -1)
        return prefs
    except Exception:
        return {}

def search_candidates(df, category=None, city=None):
    """Filter dataset by city/category before ranking."""
    if city:
        df = df[df["city"].str.contains(city, case=False, na=False)]
    if category:
        df = df[df["category"].str.contains(category, case=False, na=False)]

    # If no matches found for the city, fallback gracefully
    if df.empty and city:
        print(f"⚠️ No matches found for '{city}' — showing top-rated alternatives.")
        df = pd.read_csv("data/events_saudi.csv")
        df = df.sort_values("rating", ascending=False).head(5)

    return df.to_dict("records")


def normalize_context(context: dict) -> dict:
    """Normalize Arabic → English for city/category."""
    city_map = {"الرياض": "Riyadh"}
    category_map = {
        "عام": "general",
        "عائلي": "family",
        "ثقافي": "culture",
        "خارجي": "outdoor",
        "مطعم": "restaurant",
        "فندق": "hotel",
        "تسوق": "shopping"
    }

    c = context.copy()
    if c.get("city") in city_map:
        c["city"] = city_map[c["city"]]
    if c.get("category") in category_map:
        c["category"] = category_map[c["category"]]
    return c


# ---------------------------------------------------------------------
# Main Recommendation Flow
# ---------------------------------------------------------------------
def recommend(context: dict) -> list:
    """Recommend activities based on context and user reflection memory."""

    df = load_data()
    context = normalize_context(context)

    city = (context.get("city") or "").strip().capitalize()
    category = (context.get("category") or "general").strip().lower()

    # --- Filter logic ---
    if category == "general" or not category:
        filtered = df[df["city"].str.contains(city, case=False, na=False)]
    else:
        # Fuzzy/broad category mapping
        cat_map = {
            "family": ["park", "entertainment", "heritage", "museum", "restaurant"],
            "shopping": ["shopping", "market", "mall"],
            "culture": ["museum", "heritage", "art"],
            "outdoor": ["park", "natural", "adventure"],
            "hotel": ["hotel"],
            "restaurant": ["restaurant", "dining"],
            "general": ["entertainment", "park", "restaurant", "heritage"]
        }
        cats = cat_map.get(category, [category])
        pattern = "|".join(cats)
        filtered = df[
            df["city"].str.contains(city, case=False, na=False)
            & df["category"].str.contains(pattern, case=False, na=False)
        ]

    # --- Fallback if no results ---
    if filtered.empty:
        print("⚠️ No matches found — showing 5 top-rated activities in Riyadh.")
        filtered = df[df["city"].str.contains("Riyadh", case=False, na=False)]
        filtered = filtered.sort_values("rating", ascending=False).head(5)

    # --- Apply reflection preferences and build results ---
    prefs = _load_reflection_preferences()
    results = []
    for _, row in filtered.iterrows():
        base_score = float(row.get("rating", 0)) / 10
        bias = prefs.get(row["title"], 0)
        final_score = round(0.8 + base_score + (bias * 0.05), 2)
        final_score = min(final_score, 1.5)

        results.append({
            "title": row["title"],
            "reason": f"Category: {row['category']} | Tags: {row['tags']}",
            "score": final_score,
        })

    return results


# ---------------------------------------------------------------------
# CLI Test
# ---------------------------------------------------------------------
if __name__ == "__main__":
    ctx = {"city": "Riyadh", "category": "family"}
    results = recommend(ctx)
    print(json.dumps(results, indent=2, ensure_ascii=False))
