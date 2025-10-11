"""
Memory Agent
Manages persistent user profile memory between conversations.
"""

import json
from pathlib import Path

PROFILE_FILE = Path("data/user_profile.json")

class MemoryAgent:
    def __init__(self):
        self.profile = self._load_profile()

    def _load_profile(self):
        if PROFILE_FILE.exists():
            with open(PROFILE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_profile(self):
        PROFILE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(PROFILE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.profile, f, ensure_ascii=False, indent=2)

    def get(self, key, default=None):
        return self.profile.get(key, default)

    def update(self, key, value):
        self.profile[key] = value
        self._save_profile()

    def get_missing_fields(self):
        """Return profile keys that need to be filled."""
        required = ["name", "has_kids", "family_size", "budget_sar", "available_days", "city"]
        return [r for r in required if not self.profile.get(r)]
    
    def maybe_update_field(self, key, prompt_text=None):
        """Ask the user if they want to update an existing field."""
        current = self.profile.get(key)
        if current:
            ans = input(f"{prompt_text or f'{key}'} is currently '{current}'. Change it? (y/n): ").strip().lower()
            if ans == "y":
                new_val = input(f"Enter new value for {key}: ").strip()
                self.update(key, new_val)
                print(f"✅ Updated {key} → {new_val}")
        else:
            new_val = input(f"Please provide {key}: ").strip()
            self.update(key, new_val)
            print(f"✅ Saved {key} → {new_val}")


    def summary(self):
        """Readable summary for planner use."""
        return {
            "name": self.profile.get("name"),
            "has_kids": self.profile.get("has_kids"),
            "family_size": self.profile.get("family_size"),
            "budget_sar": self.profile.get("budget_sar"),
            "available_days": self.profile.get("available_days"),
            "city": self.profile.get("city")
        }
       