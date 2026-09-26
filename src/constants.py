"""All URLs, user-facing messages, and system prompts for the travel chatbot."""

# ---------- URLs ----------

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

# ---------- System prompts ----------

SYSTEM_PROMPT = """You are a friendly one-day travel planner chatbot.

When a user names a city (or asks you to plan/adjust a trip), do this in order,
actually calling the tools:
1. Use the get_weather tool for the city's current weather.
2. Use the tavily tool to search "top 3 popular tourist attractions in <city>".
3. Estimate typical per-person costs in USD (entry fees, local transport,
   meals) and use the calculator tool to add them into one total.
4. Reply with a concise one-day itinerary:
   - Weather line
   - Morning / Afternoon / Evening schedule naming the 3 attractions
   - Cost breakdown with the final total

Be conversational on follow-ups: if the user asks to make it cheaper, swap an
attraction, or change the city, reuse tool results when possible and recompute
costs with the calculator. If a city is unknown or misspelled, ask the user to
clarify instead of guessing."""

# ---------- Messages ----------

WEATHER_NOT_FOUND = "Weather not found for city '{city}'. Please check the spelling."

WEATHER_SUMMARY = "Current weather in {name}: {temp:.1f}C (feels like {feels:.1f}C), {desc}."

CHAT_ERROR = (
    "Sorry, something went wrong while planning: {exc}\n"
    "Please try again or name another city."
)

UI_TITLE = "Strands Travel Planner"

UI_DESCRIPTION = (
    "Tell me a city and I'll check the weather, find 3 attractions, "
    "estimate your costs, and build a one-day itinerary."
)

UI_EXAMPLES = ["Plan a one-day trip to Kathmandu", "Plan a day in Tokyo"]

GREETING_MESSAGE = (
    "Hello! I am your friendly Strands Travel Planner Chatbot, here to assist you. "
    "Tell me a city and I'll plan a one-day trip: weather, top 3 attractions, "
    "and a cost breakdown. For example, try: \"Plan a one-day trip to Kathmandu\"."
)

WHOAMI_MESSAGE = (
    "I'm the Strands Travel Planner Chatbot! I check the weather, find the top "
    "3 attractions in any city, estimate costs, and build you a one-day "
    "itinerary. Just name a city to get started."
)

THANKS_MESSAGE = (
    "You're welcome! Happy travels. If you'd like another city or a cheaper "
    "plan, just say the word."
)

GREETING_PATTERNS = [
    ("hello", GREETING_MESSAGE),
    ("hi", GREETING_MESSAGE),
    ("hey", GREETING_MESSAGE),
    ("good morning", GREETING_MESSAGE),
    ("good afternoon", GREETING_MESSAGE),
    ("good evening", GREETING_MESSAGE),
    ("who are you", WHOAMI_MESSAGE),
    ("what can you do", WHOAMI_MESSAGE),
    ("help", GREETING_MESSAGE),
    ("thank", THANKS_MESSAGE),
    ("thanks", THANKS_MESSAGE),
]
