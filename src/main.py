"""Assignment 2: Strands Travel Planner.

Builds a one-day travel plan for a given city:
1. Weather tool  -> current weather (OpenWeather)
2. Search tool   -> 3 popular attractions (DuckDuckGo)
3. Calculator    -> total estimated cost (built-in strands_tools.calculator)
4. Agent combines everything into a one-day itinerary.
"""

import sys

import requests

from constants import (
    LLM_API_KEY,
    LLM_BASE_URL,
    LLM_MODEL,
    MODEL_REASONING_EFFORT,
    MODEL_TEMPERATURE,
    OPENWEATHER_API_KEY,
    OPENWEATHER_URL,
    PROMPT,
    REQUEST_TIMEOUT_SECONDS,
)

from strands import Agent, tool
from strands.models.openai import OpenAIModel
from strands_tools import calculator, tavily


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
        OPENWEATHER_URL,
        params={"q": city, "units": "metric", "appid": OPENWEATHER_API_KEY},
        timeout=REQUEST_TIMEOUT_SECONDS,
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
    params={
        "temperature": MODEL_TEMPERATURE,
        "reasoning_effort": MODEL_REASONING_EFFORT,
    },
)

agent = Agent(model=MODEL, tools=[get_weather, tavily, calculator])


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python src/main.py <city>")
        sys.exit(1)
    city = " ".join(sys.argv[1:])
    print(agent(PROMPT.format(city=city)))


if __name__ == "__main__":
    main()