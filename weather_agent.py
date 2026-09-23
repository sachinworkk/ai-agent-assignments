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

MODEL = "gemini-flash-lite-latest"
MAX_TOOL_ROUNDS = 5  # safety cap on the tool-calling loop

LOCATIONS = ["Kathmandu", "Delhi", "London"]

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not GEMINI_API_KEY:
    raise SystemExit("GEMINI_API_KEY missing — copy .env.example to .env and fill it in.")
if not OPENWEATHER_API_KEY:
    raise SystemExit("OPENWEATHER_API_KEY missing — copy .env.example to .env and fill it in.")

client = genai.Client()


# ---------------------------------------------------------------------------
# Tool 1: OpenWeather current-weather lookup
# ---------------------------------------------------------------------------
def get_current_weather(city: str) -> dict:
    """Returns the current temperature (Celsius) and conditions for a city.

    Args:
        city: The city name to look up (e.g. 'Kathmandu', 'London').
    """
    print(f"[TOOL] Fetching current weather for '{city}'...")
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
        system_instruction=(
            "You are a weather assistant. You MUST call get_current_weather for "
            "each requested location, one location at a time. Do not skip any "
            "location and do not invent temperatures."
        ),
        tools=[get_current_weather],
        temperature=0.0,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )

    prompt = (
        f"What is the current weather in {', '.join(cities)}? "
        "Call the weather tool for each location one at a time."
    )
    contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]

    weather_results: list[dict] = []

    for round_no in range(1, MAX_TOOL_ROUNDS + 1):
        response = client.models.generate_content(
            model=MODEL, contents=contents, config=config
        )
        contents.append(response.candidates[0].content)
        function_calls = response.function_calls
        if not function_calls:
            print("\n--- Agent summary ---")
            print(response.text)
            break

        for call in function_calls:
            fn_name = call.name or ""
            fn_args = dict(call.args) if call.args else {}
            print(f"[AGENT] Requested tool: {fn_name} with args {fn_args}")
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
        print("Stopped: reached the tool-round cap without a final answer.")

    # Average computed in Python — never trust the LLM with arithmetic.
    print("\n--- Collected temperatures ---")
    temps = [w["temperature_c"] for w in weather_results]
    for w in weather_results:
        print(f"{w['city']}: {w['temperature_c']}°C ({w['conditions']})")
    if len(temps) == len(cities) and temps:
        avg = sum(temps) / len(temps)
        print(f"\nAverage temperature across {len(temps)} locations: {avg:.2f}°C")
    else:
        print(f"\nCould not compute average: got {len(temps)}/{len(cities)} results.")


if __name__ == "__main__":
    run_weather_agent(LOCATIONS)
