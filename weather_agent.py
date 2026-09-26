"""Assignment 1: Weather Agent.

Gemini SDK agent that retrieves the current weather for three locations using
OpenWeather. Weather API calls are made sequentially via manual function
calling (AFC disabled), then the average temperature is computed in Python.
"""

import os

import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types

from constants import (
    ERR_MISSING_GEMINI_KEY,
    ERR_MISSING_OPENWEATHER_KEY,
    LOCATIONS,
    MAX_TOOL_ROUNDS,
    MODEL,
    MSG_AGENT_REQUEST,
    MSG_AGENT_SUMMARY,
    MSG_AVERAGE,
    MSG_COLLECTED,
    MSG_INCOMPLETE,
    MSG_ROUND_CAP,
    MSG_TEMP_LINE,
    MSG_TOOL_FETCH,
    PROMPT_TEMPLATE,
    SYSTEM_INSTRUCTION,
)

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not GEMINI_API_KEY:
    raise SystemExit(ERR_MISSING_GEMINI_KEY)
if not OPENWEATHER_API_KEY:
    raise SystemExit(ERR_MISSING_OPENWEATHER_KEY)

client = genai.Client()


# ---------------------------------------------------------------------------
# Tool 1: OpenWeather current-weather lookup
# ---------------------------------------------------------------------------
def get_current_weather(city: str) -> dict:
    """Returns the current temperature (Celsius) and conditions for a city.

    Args:
        city: The city name to look up (e.g. 'Kathmandu', 'London').
    """
    print(MSG_TOOL_FETCH.format(city=city))
    try:
        resp = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"},
            timeout=10,
        )
        if resp.status_code == 404:
            return {"error": f"City '{city}' not found."}
        if resp.status_code == 401:
            return {"error": "Invalid or not-yet-active OpenWeather API key."}
        resp.raise_for_status()
        data = resp.json()
        return {
            "city": data.get("name", city),
            "temperature_c": data["main"]["temp"],
            "conditions": data["weather"][0]["description"],
        }
    except requests.RequestException as exc:
        return {"error": f"Weather request failed for '{city}': {exc}"}


available_tools = {"get_current_weather": get_current_weather}


# ---------------------------------------------------------------------------
# Agent loop: manual function calling, one call per round => sequential
# ---------------------------------------------------------------------------
def run_weather_agent(cities: list[str]) -> None:
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        tools=[get_current_weather],
        temperature=0.0,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )

    prompt = PROMPT_TEMPLATE.format(cities=", ".join(cities))
    contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]

    weather_results: list[dict] = []

    for round_no in range(1, MAX_TOOL_ROUNDS + 1):
        response = client.models.generate_content(
            model=MODEL, contents=contents, config=config
        )
        candidate = response.candidates[0] if response.candidates else None
        if candidate is None or candidate.content is None:
            print(f"Stopped: model returned no content in round {round_no}.")
            break
        contents.append(candidate.content)
        function_calls = response.function_calls
        if not function_calls:
            print(MSG_AGENT_SUMMARY)
            print(response.text)
            break

        for call in function_calls:
            fn_name = call.name or ""
            fn_args = dict(call.args) if call.args else {}
            print(MSG_AGENT_REQUEST.format(fn_name=fn_name, fn_args=fn_args))
            fn = available_tools.get(fn_name)
            result = fn(**fn_args) if fn else {"error": f"Unknown tool '{fn_name}'"}
            if isinstance(result, dict) and "temperature_c" in result:
                weather_results.append(result)
            contents.append(
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_function_response(
                            name=fn_name, response=result
                        )
                    ],
                )
            )
    else:
        print(MSG_ROUND_CAP)

    # Average computed in Python — never trust the LLM with arithmetic.
    print(MSG_COLLECTED)
    temps = [w["temperature_c"] for w in weather_results]
    for w in weather_results:
        print(MSG_TEMP_LINE.format(city=w["city"], temp=w["temperature_c"], conditions=w["conditions"]))
    if len(temps) == len(cities) and temps:
        avg = sum(temps) / len(temps)
        print(MSG_AVERAGE.format(count=len(temps), avg=f"{avg:.2f}"))
    else:
        print(MSG_INCOMPLETE.format(got=len(temps), expected=len(cities)))


if __name__ == "__main__":
    run_weather_agent(LOCATIONS)
