"""Constants for the Strands Travel Planner.

Environment-derived configuration, external API endpoints, and the
agent prompt live here so main.py stays focused on wiring the agent.
"""

import os

from dotenv import load_dotenv

load_dotenv()

# ---------- Environment / API keys ----------

OPENWEATHER_API_KEY = os.environ["OPENWEATHER_API_KEY"]
LLM_BASE_URL = os.environ["LLM_BASE_URL"]
LLM_MODEL = os.environ["LLM_MODEL"]
LLM_API_KEY = os.environ["LLM_API_KEY"] or os.environ.get("OPENROUTER_API_KEY")

# ---------- External API endpoints ----------

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
REQUEST_TIMEOUT_SECONDS = 15

# ---------- Agent ----------

MODEL_TEMPERATURE = 0.4
MODEL_REASONING_EFFORT = "low"

PROMPT = """Plan a one-day trip to {city}.

Follow these steps in order and actually call the tools:
1. Use the get_weather tool to check the current weather in {city}.
2. Use the tavily tool to search for "top 3 popular tourist attractions in {city}".
3. Estimate typical per-person costs in USD (entry fees, local transport,
   meals) and use the calculator tool to add them into one total.
4. Combine everything into a concise one-day itinerary:
   - Weather line
   - Morning / Afternoon / Evening schedule naming the 3 attractions
   - Cost breakdown with the final total

Weather and attractions results:
"""