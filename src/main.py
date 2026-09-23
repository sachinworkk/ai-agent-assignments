"""Assignment 2: Strands Travel Planner.

Builds a one-day travel plan for a given city:
1. Weather tool  -> current weather (OpenWeather)
2. Search tool   -> 3 popular attractions (DuckDuckGo)
3. Calculator    -> total estimated cost (built-in strands_tools.calculator)
4. Agent combines everything into a one-day itinerary.
"""

import os
import sys

import requests
from dotenv import load_dotenv

from strands import Agent, tool
from strands.models.openai import OpenAIModel
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
        return f"Weather not found for city '{city}'."
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

agent = Agent(model=MODEL, tools=[get_weather, tavily, calculator])

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


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python src/main.py <city>")
        sys.exit(1)
    city = " ".join(sys.argv[1:])
    print(agent(PROMPT.format(city=city)))


if __name__ == "__main__":
    main()
