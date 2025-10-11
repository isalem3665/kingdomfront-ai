# src/agents/reflection_agent.py
import json
from datetime import datetime
from pathlib import Path

MEMORY_FILE = Path("data/reflection_memory.json")

class ReflectionAgent:
    def __init__(self):
        self.memory = self._load_memory()

    def _load_memory(self):
        if MEMORY_FILE.exists():
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"interactions": []}

    def _save_memory(self):
        MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)

    def log_interaction(self, query, response, feedback=None):
        """Store a user interaction and feedback"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response,
            "feedback": feedback
        }
        self.memory["interactions"].append(entry)
        self._save_memory()

    def reflect(self):
        """Analyze memory and generate insights"""
        if not self.memory["interactions"]:
            return "No past interactions yet."

        accepted = [
            i for i in self.memory["interactions"]
            if i.get("feedback") == "positive"
        ]
        rejected = [
            i for i in self.memory["interactions"]
            if i.get("feedback") == "negative"
        ]

        summary = {
            "total": len(self.memory["interactions"]),
            "positive": len(accepted),
            "negative": len(rejected),
            "insight": self._generate_insight(accepted, rejected)
        }

        return summary

    def _generate_insight(self, accepted, rejected):
        if not accepted and not rejected:
            return "User preferences not yet established."
        if len(accepted) > len(rejected):
            return "User tends to prefer cultural or relaxing activities."
        else:
            return "User tends to prefer energetic or social activities."
