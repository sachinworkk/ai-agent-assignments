# Assignment 1: Weather Agent

Build an AI agent using the **Gemini SDK** that retrieves the current weather for
three specified locations using OpenWeather. The agent makes the weather API
calls **sequentially**, collects the temperature from each location, and
calculates and displays the **average temperature** across all three locations.

## Plan

- Tool: `get_current_weather(city)` → OpenWeather current-weather API (metric).
- Agent: Gemini (`gemini-2.0-flash`) with manual function calling
  (AFC disabled) so each tool call is visible and sequential.
- Average: computed in Python from the collected tool results, not by the LLM.

## Setup

```bash
python -m pip install google-genai python-dotenv requests
```

Create a `.env` file (see `.env.example`) with:

- `GEMINI_API_KEY`
- `OPENWEATHER_API_KEY`

Note: new OpenWeather API keys take ~10 minutes to a couple of hours to
activate — a 401 right after signup is normal.

## Usage

```bash
python weather_agent.py
```