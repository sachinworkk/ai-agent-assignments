"""Assignment 3: Strands Travel Planner Chatbot.

Interactive Gradio chatbot that plans a one-day trip for any city:
1. Weather tool  -> current weather (OpenWeather)
2. Search tool   -> 3 popular attractions (Tavily)
3. Calculator    -> total estimated cost (built-in strands_tools.calculator)
4. Agent combines everything into a one-day itinerary, delivered in chat.

Model provider: OpenRouter (OpenAI-compatible) using gpt-oss-20b.
"""

import os

import gradio as gr
import requests
from dotenv import load_dotenv

from strands import Agent, tool
from strands.models.openai import OpenAIModel
from strands.session.file_session_manager import FileSessionManager
from strands_tools import calculator, tavily

load_dotenv()

OPENWEATHER_API_KEY = os.environ["OPENWEATHER_API_KEY"]
LLM_BASE_URL = os.environ["LLM_BASE_URL"]
LLM_MODEL = os.environ["LLM_MODEL"]
LLM_API_KEY = os.environ["LLM_API_KEY"] or os.environ.get("OPENROUTER_API_KEY")


# ---------- Tools ----------

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city using OpenWeather.

    Args:
        city: City name, e.g. "Kathmandu".

    Returns:
        Human-readable summary of current temperature and conditions.
    """
    resp = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={"q": city, "units": "metric", "appid": OPENWEATHER_API_KEY},
        timeout=15,
    )
    if resp.status_code == 404:
        return f"Weather not found for city '{city}'. Please check the spelling."
    resp.raise_for_status()
    data = resp.json()
    temp = data["main"]["temp"]
    feels = data["main"]["feels_like"]
    desc = data["weather"][0]["description"]
    name = data["name"]
    return (
        f"Current weather in {name}: {temp:.1f}C (feels like {feels:.1f}C), {desc}."
    )


# ---------- Agent ----------

MODEL = OpenAIModel(
    client_args={"api_key": LLM_API_KEY, "base_url": LLM_BASE_URL},
    model_id=LLM_MODEL,
    params={"temperature": 0.4, "reasoning_effort": "low"},
)

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

agent = Agent(
    model=MODEL,
    tools=[get_weather, tavily, calculator],
    system_prompt=SYSTEM_PROMPT,
)


def chat(message: str, history: list) -> str:
    """Gradio chat handler: routes every message through the Strands agent.

    The agent's conversation is persisted per browser session so follow-ups
    ("make it cheaper") keep context.
    """
    del history  # Gradio supplies it; the Strands agent keeps its own context.
    try:
        return str(agent(message))
    except Exception as exc:  # noqa: BLE001 - user-facing error handling
        return (
            f"Sorry, something went wrong while planning: {exc}\n"
            "Please try again or name another city."
        )


demo = gr.ChatInterface(
    fn=chat,
    type="messages",
    title="Strands Travel Planner",
    description=(
        "Tell me a city and I'll check the weather, find 3 attractions, "
        "estimate your costs, and build a one-day itinerary."
    ),
    examples=["Plan a one-day trip to Kathmandu", "Plan a day in Tokyo"],
    theme=gr.themes.Soft(),
)


if __name__ == "__main__":
    demo.launch()
