"""
Cognitive Orchestrator v3
Conversation → Memory → Recommendation → Planner → Reflection → (Optional) Booking
Smart hotel logic with detection for staying with friends/family.
"""

import argparse
import json
import time
import re

from conversation_agent import extract_intent
from recommendation_agent import recommend
from reflection_agent import ReflectionAgent
from memory_agent import MemoryAgent
from planner_agent import PlannerAgent
from booking_agent import BookingAgent
from pathlib import Path
import pandas as pd


def _safe_print_json(title: str, payload: dict | list):
    print(f"\n[{title}]")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def detect_stay_with_friends(query: str) -> bool:
    """
    Detect if user mentions staying with friends or family.
    Works in Arabic and English.
    """
    keywords = [
        r"\bfriends?\b", r"\bfamily\b", r"\brelative", r"\bparents", r"\bhome\b",
        r"صديق", r"أصدق", r"عائلة", r"أسرتي", r"عند أهلي", r"عند أصدقائي"
    ]
    return any(re.search(k, query.lower()) for k in keywords)


def run_pipeline(query: str):
    t0 = time.time()

    # ── Step 1: Initialize agents
    reflection = ReflectionAgent()
    memory = MemoryAgent()

    # ── Step 2: Ask missing profile data (one-time bootstrap)
    missing = memory.get_missing_fields()
    if missing:
        print("🤔 I need some info first to personalize your trip:")
        for field in missing:
            answer = input(f"Please provide {field.replace('_',' ')}: ")
            memory.update(field, answer)
        print("✅ Thanks! Your profile has been saved.\n")

    # ── Quick interactive updates for common fields (optional)
    for field in ["available_days", "budget_sar", "city"]:
        memory.maybe_update_field(field, prompt_text=f"{field.replace('_', ' ')}")

    # ── Step 3: Extract intent and merge with memory profile
    intent_data = extract_intent(query)
    intent = intent_data.get("intent")
    context = intent_data.get("context", {}) or {}

    if not context:
        context = {
            "city": intent_data.get("city"),
            "category": intent_data.get("category"),
            "budget_sar": intent_data.get("budget_sar"),
            "time": intent_data.get("time"),
        }

    profile_summary = memory.summary()
    context.update({k: v for k, v in profile_summary.items() if v is not None})

    # ── Step 4: Get recommendations strictly from CSV
    recs = recommend(context)

    # ── Step 5: Auto feedback & reflection log
    avg_score = (sum([r.get("score", 0) for r in recs]) / len(recs)) if recs else 0.0
    feedback = "positive" if avg_score >= 0.8 else "negative"
    reflection.log_interaction(query, recs, feedback)

    # ── Step 6: Detect stage and create itinerary
    try:
        from planner_stage import PlannerStageClassifier
        stage = PlannerStageClassifier(context).detect_stage()
    except ImportError:
        stage = "default"

    planner = PlannerAgent(profile_summary, stage=stage)
    plan = planner.create_plan(recs)

    # ── Step 7: Build result before any hotel decisions
    result = {
        "intent": intent,
        "context": context,
        "feedback": feedback,
        "itinerary": plan,
        "latency_sec": round(time.time() - t0, 2),
    }

    # ── Step 8: Show plan first (no booking yet)
    _safe_print_json("🧠 Personalized Plan", plan)
    _safe_print_json("Reflection Summary", reflection.reflect())

    # ── Step 9: Smart hotel handling
    user_home_city = (memory.summary().get("city") or "").lower()
    trip_city = (context.get("city") or "").lower()
    stage = plan.get("stage", "default")

    # --- Detect “staying with friends or family” ---
    staying_with_friends = detect_stay_with_friends(query)
    if staying_with_friends:
        print("🏡 Detected that you plan to stay with friends/family — hotel skipped.")
        return result

    include_hotels = False
    if stage == "travel" or trip_city != user_home_city:
        # User is traveling outside home city
        try:
            hotel_needed = input(
                f"\nYou’re planning a trip to {trip_city.title()}. "
                "Would you like to include hotel stays? (y/n): "
            ).strip().lower()
        except EOFError:
            hotel_needed = "n"

        include_hotels = hotel_needed == "y"
    else:
        print("🏠 Local plan detected — no hotels required.")
        include_hotels = False

    # ── Step 10: Add hotel to plan if user requested
    if include_hotels:

        

        try:
            # --- define upfront ---
            hotels_df = pd.DataFrame()
            hotel_name = None

            # --- dataset path ---
            DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "events_riyadh_clean.csv"
            if not DATA_PATH.exists():
                raise FileNotFoundError(f"❌ Dataset not found at {DATA_PATH.resolve()}")

            # --- load dataset ---
            df = pd.read_csv(DATA_PATH, on_bad_lines="skip")
            if "category" not in df.columns or "city" not in df.columns:
                raise ValueError("❌ Dataset is missing required columns: 'category' or 'city'")

            # --- filter hotels ---
            hotels_df = df[df["category"].str.contains("hotel", case=False, na=False)]

            if hotels_df.empty:
                print("⚠️ No hotels found in dataset.")
            else:
                # --- filter by target city ---
                city_hotels = hotels_df[hotels_df["city"].str.contains(trip_city, case=False, na=False)]
                if city_hotels.empty:
                    print(f"⚠️ No hotels found for '{trip_city}' — picking a random hotel from dataset.")
                    city_hotels = hotels_df.sample(1)

                # --- pick first hotel ---
                    hotel_name = city_hotels.iloc[0]["title"]
                    last_day = f"Day {int(plan['days'])}"
                    plan["itinerary"].setdefault(last_day, {})
                    plan["itinerary"][last_day]["Evening"] = hotel_name
                    print(f"🏨 Added hotel '{hotel_name}' to your itinerary.")

        except Exception as e:
            print(f"⚠️ Could not load hotel data safely: {e}")






        
        # Ask whether to confirm booking
        try:
            confirm = input("\nWould you like to confirm hotel bookings now? (y/n): ").strip().lower()
        except EOFError:
            confirm = "n"

        if confirm == "y":
            booking = BookingAgent()
            booked_hotels = set()
            booked_days = set()

            day_to_slots = (plan or {}).get("itinerary", {}) or {}
            for day, schedule in day_to_slots.items():
                if day in booked_days:
                    continue
                for period in ["Morning", "Afternoon", "Evening"]:
                    place = schedule.get(period)
                    if not place:
                        continue
                    if any(
                        kw in place.lower()
                        for kw in ["hotel", "hilton", "inn", "ritz", "fairmont", "movenpick", "intercontinental",
                                    "radisson", "marriott", "novotel", "crowne", "ibis", "holiday", "sheraton"]

                    ):
                        if place not in booked_hotels:
                            booking.book(
                                user_name=context.get("name", "Guest"),
                                item=place,
                                date=f"{day} - {period}",
                                price=0,
                            )
                            booked_hotels.add(place)
                            booked_days.add(day)
                            break

            if not booked_hotels:
                print("ℹ️ No hotel-like entries detected, nothing booked.")
        else:
            print("🕓 Booking skipped for now.")
    else:
        print("🏠 Staying local or skipping hotel stay — no hotel added.")

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cognitive Orchestrator v3")
    parser.add_argument("--query", type=str, required=True, help="User question")
    args = parser.parse_args()

    output = run_pipeline(args.query)
    _safe_print_json("Pipeline Output", output)
