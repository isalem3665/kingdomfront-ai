"""
Booking Agent
Handles hotel or activity bookings based on the user itinerary/context.
Currently simulated (prints confirmation instead of calling real APIs).
"""

import json
from datetime import datetime

class BookingAgent:
    def __init__(self):
        self.bookings_file = "data/bookings_log.json"

    def book(self, user_name: str, item: str, date: str, price: float = 0):
        """Simulate a booking for a hotel or activity."""
        record = {
            "user": user_name,
            "item": item,
            "date": date,
            "price": price,
            "status": "confirmed",
            "timestamp": datetime.now().isoformat()
        }
        self._save_booking(record)
        print(f"✅ Booking confirmed for '{item}' on {date} for {user_name}.")
        return record

    def _save_booking(self, record):
        try:
            with open(self.bookings_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = []

        data.append(record)
        with open(self.bookings_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
