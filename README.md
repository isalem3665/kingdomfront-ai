# 🧠 Kingdom Front – Agentic AI Core (Mini-MVP)

## 🏰 Overview
This repository hosts the **AI brain of Kingdom Front**, an **agentic travel and lifestyle assistant**.  
The Mini-MVP demonstrates **autonomous reasoning** and **memory-driven personalization** across the full cognitive cycle:

> **Understand → Search → Recommend → Plan → Reflect → (Book)**

The **Cognitive Orchestrator** coordinates multiple cooperative agents that personalize itineraries, activities, and decisions for each user.

---

## 🏗️ Architecture

### 🧩 Core Flow
1. **Understand:** Parse user intent and extract contextual data.  
2. **Search:** Retrieve relevant activities and experiences.  
3. **Recommend:** Rank options using user profile and reflection bias.  
4. **Plan:** Construct itineraries across local or travel contexts.  
5. **Reflect:** Learn from past interactions to improve recommendations.  
6. **Book:** Simulate booking and confirmation flow (optional).

---

### 🤖 Agent Roles

| Agent | Description |
|--------|-------------|
| 🗣️ **ConversationAgent** | Extracts user intent and key context (city, category, budget, time). |
| 💾 **MemoryAgent** | Stores and updates the user profile (name, city, family size, etc.). |
| 🎯 **RecommendationAgent** | Retrieves the best-matching activities from datasets and applies reflection bias. |
| 🧭 **PlannerAgent** | Builds itineraries based on the detected stage (local, travel, family, friends, or default). |
| 🪞 **ReflectionAgent** | Learns from previous interactions and adjusts recommendations accordingly. |
| 🏨 **BookingAgent** | Simulates hotel bookings and confirmation logic. |

---

### 🌍 Planner Stages

| Stage | Description | Example Query |
|-------|--------------|----------------|
| 🏠 **Local** | Short in-city plan (no hotels). | `اريد خطة نهاية الأسبوع في الرياض` |
| ✈️ **Travel** | Multi-day trip with hotel options. | `اريد خطة ليومين في جدة` |
| 👨‍👩‍👧 **Family** | Family-focused activities (parks, museums, kid-friendly). | `اريد خطة عائلية في الرياض` |
| 👬 **Friends** | Social or cultural activities (no hotel). | `سأزور أصدقائي في الدمام` |
| 🌍 **Default** | Generic mixed plan for broad exploration. | `وش نسوي اليوم؟` |

---

## ⚙️ Setup & Usage

### 1. Clone the Repository
```bash
git clone https://github.com/Hamadalnamazi/kingdomfront-ai.git
cd kingdomfront-ai
```
```bash
python src/orchestrator.py --query "وش نسوي اليوم بالرياض؟"
```
```bash
kingdomfront-ai/
 ├── data/
 │   ├── events_riyadh_clean.csv        # Local attractions and experiences
 │   └── reflection_memory.json         # Reflection and learning memory store
 ├── src/
 │   ├── orchestrator.py                # Main orchestrator connecting all agents
 │   ├── conversation_agent.py          # Intent extraction and context detection
 │   ├── memory_agent.py                # Profile memory manager
 │   ├── recommendation_agent.py        # Recommendation engine
 │   ├── planner_agent.py               # Itinerary and stage planner
 │   ├── planner_stage.py               # Stage rules (local, travel, etc.)
 │   ├── reflection_agent.py            # Learning and feedback logic
 │   └── booking_agent.py               # Booking simulation
 ├── requirements.txt
 └── README.md
```
```bash
python src/orchestrator.py --query "اريد خطة عائلية في الرياض"
```
```bash
Maintained by: Hamad Alnamazi 
Status: 🟡 In Development (Mini-MVP Phase)
License: Proprietary © 2025
```