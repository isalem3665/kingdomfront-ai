"""
Planner Agent (Final Version)
Builds realistic itineraries and ensures only one hotel per trip.
"""

from random import shuffle
import pandas as pd


class PlannerAgent:
    def __init__(self, user_profile, stage="default"):
        self.profile = user_profile
        self.stage = stage

    def _parse_duration(self, text):
        """Convert text like '2', 'two days', or '2 hours' into day count."""
        import re
        if not text:
            return 1
        match = re.search(r"(\d+)", str(text))
        num = int(match.group(1)) if match else 1
        text_lower = str(text).lower()
        if "hour" in text_lower or "ساعة" in text_lower:
            return max(0.25, num / 24)
        return max(1, num)

    def create_plan(self, recommendations):
        """Generate realistic, stage-based itinerary with at most one hotel."""
        days = self._parse_duration(self.profile.get("available_days", 1))
        name = self.profile.get("name", "Traveler")
        city = self.profile.get("city", "Riyadh")

        if not recommendations:
            return {
                "user": name,
                "city": city,
                "days": days,
                "itinerary": {},
                "note": f"عذرًا {name}، لا توجد أنشطة كافية للتخطيط الآن."
            }

        # --- Separate hotels from other activities
        hotels = [r for r in recommendations if "hotel" in r.get("category", "").lower()]
        others = [r for r in recommendations if r not in hotels]

        # --- Choose only one hotel (best-rated) if any exist
        best_hotel = None
        if hotels:
            best_hotel = sorted(hotels, key=lambda x: x.get("rating", 0), reverse=True)[0]

        # --- Shuffle other activities for variety
        shuffle(others)

        plan = {"user": name, "city": city, "days": days, "stage": self.stage, "itinerary": {}}

        # --- Short plan (<1 day)
        if days < 1:
            slots = ["Afternoon", "Evening"]
            for i, slot in enumerate(slots):
                if i < len(others):
                    plan["itinerary"][slot] = others[i]["title"]
            if best_hotel:
                plan["itinerary"]["Evening"] = best_hotel["title"]
            return plan

        # --- Multi-day itinerary
        per_day = max(1, int(round(len(others) / days)))
        idx = 0
        for d in range(int(days)):
            day_key = f"Day {d+1}"
            day_acts = others[idx:idx + 3]
            idx += 3

            plan["itinerary"][day_key] = {
                "Morning": day_acts[0]["title"] if len(day_acts) > 0 else None,
                "Afternoon": day_acts[1]["title"] if len(day_acts) > 1 else None,
                "Evening": day_acts[2]["title"] if len(day_acts) > 2 else None,
            }

        # --- Add one hotel only on the final evening
        if best_hotel:
            last_day = f"Day {int(days)}"
            plan["itinerary"].setdefault(last_day, {})
            plan["itinerary"][last_day]["Evening"] = best_hotel["title"]

        return plan
