"""Shared constants for the Gemini weather agent and chatbot."""

# ---------------------------------------------------------------------------
# Model / loop config
# ---------------------------------------------------------------------------
MODEL = "gemini-flash-lite-latest"  # lite alias = highest free-tier rate limit
MAX_TOOL_ROUNDS = 5  # safety cap on the tool-calling loop

# ---------------------------------------------------------------------------
# Locations
# ---------------------------------------------------------------------------
LOCATIONS = ["Kathmandu", "Delhi", "London"]

# ---------------------------------------------------------------------------
# Prompts / system instruction
# ---------------------------------------------------------------------------
SYSTEM_INSTRUCTION = (
    "You are a weather assistant. You MUST call get_current_weather for "
    "each requested location, one location at a time. Do not skip any "
    "location and do not invent temperatures."
)

PROMPT_TEMPLATE = (
    "What is the current weather in {cities}? "
    "Call the weather tool for each location one at a time."
)

# ---------------------------------------------------------------------------
# Console messages
# ---------------------------------------------------------------------------
MSG_TOOL_FETCH = "[TOOL] Fetching current weather for '{city}'..."
MSG_AGENT_REQUEST = "[AGENT] Requested tool: {fn_name} with args {fn_args}"
MSG_AGENT_SUMMARY = "\n--- Agent summary ---"
MSG_ROUND_CAP = "Stopped: reached the tool-round cap without a final answer."
MSG_NO_CONTENT = "Stopped: model returned no content in round {round_no}."
MSG_COLLECTED = "\n--- Collected temperatures ---"
MSG_TEMP_LINE = "{city}: {temp}°C ({conditions})"
MSG_AVERAGE = "\nAverage temperature across {count} locations: {avg}°C"
MSG_INCOMPLETE = "\nCould not compute average: got {got}/{expected} results."

# ---------------------------------------------------------------------------
# Error messages
# ---------------------------------------------------------------------------
ERR_MISSING_GEMINI_KEY = (
    "GEMINI_API_KEY missing — copy .env.example to .env and fill it in."
)
ERR_MISSING_OPENWEATHER_KEY = (
    "OPENWEATHER_API_KEY missing — copy .env.example to .env and fill it in."
)
