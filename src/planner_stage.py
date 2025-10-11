"""
PlannerStageClassifier
Detects which planning stage applies based on context and user intent.
"""

class PlannerStageClassifier:
    def __init__(self, context):
        self.ctx = context or {}

    def detect_stage(self):
        city = (self.ctx.get("city") or "").lower()
        days = float(self.ctx.get("available_days") or 1)
        has_kids = int(self.ctx.get("has_kids") or 0)
        time = (self.ctx.get("time") or "").lower()
        intent = (self.ctx.get("intent") or "").lower()

        # Local / home weekend
        if "weekend" in time or days <= 1:
            return "local"

        # Travel to another city
        if city not in ["riyadh", "الرياض"] and days > 1:
            return "travel"

        # Family focus
        if has_kids == 1 or "kids" in intent or "عائلة" in intent:
            return "family"

        # Visiting friends
        if "visit" in intent or "صديق" in intent or "الأصدقاء" in intent:
            return "friends"

        # Default
        return "default"
