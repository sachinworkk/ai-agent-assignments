# Assignment 1: Weather Agent

Build an AI agent using the **Gemini SDK** that retrieves the current weather for
three specified locations using OpenWeather. The agent makes the weather API
calls **sequentially**, collects the temperature from each location, and
calculates and displays the **average temperature** across all three locations.

The whole workflow is a Jupyter notebook: `weather_agent.ipynb`. Open it and run
the cells top to bottom — each step (config, sanity check, tool, agent loop,
final run) is explained in markdown with expected output shown inline.

## How it works

- Tool: `get_current_weather(city)` → OpenWeather current-weather API (metric).
- Agent: Gemini (`gemini-flash-lite-latest`) with **manual function calling**
  (AFC disabled), so Gemini returns each tool call and our loop executes it —
  every call is visible and strictly sequential.
- Average: computed in Python from the collected tool results, not by the LLM.

## Setup

```bash
python -m pip install google-genai python-dotenv requests
```

Create a `.env` file at the repo root (see `../.env.example`) with:

- `GEMINI_API_KEY`
- `OPENWEATHER_API_KEY`

Note: new OpenWeather API keys take ~10 minutes to a couple of hours to
activate — a 401 right after signup is normal.

## Usage

```bash
jupyter notebook weather_agent.ipynb
```

(If Jupyter isn't installed: `python -m pip install notebook`.)

### Cell-by-cell walkthrough

| Cell | What it does |
|---|---|
| 1 (code) | Imports, loads `.env`, checks both API keys are set |
| 2 (code) | Loads shared config from `constants.py` (model, locations, prompts) |
| 3 (code) | Sanity check — a minimal chatbot round-trip to verify the Gemini key (was `chatbot.py`) |
| 4 (code) | Defines `get_current_weather(city)` and calls it directly for one city |
| 5 (code) | Defines `run_weather_agent()` — the manual sequential tool-calling loop |
| 6 (code) | Runs the agent on all three locations and prints the average temperature |

Every markdown cell above a code cell explains the step and shows the expected
output, so a reviewer can follow the workflow without running anything.
