# Strands Travel Planner (Assignment 2)

AI agent built with [Strands Agents](https://github.com/strands-agents/sdk-python)
that plans a one-day trip for a city: checks current weather, finds 3 popular
attractions, estimates total visit cost, and writes a one-day itinerary.

The whole workflow is a Jupyter notebook: `travel_planner.ipynb`. Open it and run
the cells top to bottom — each step (config, tool, agent wiring, final run) is
explained in markdown with expected output shown inline.

## How it works

- `get_weather` — custom Strands `@tool`, current weather via OpenWeather
- `search_attractions` — web search for 3 popular attractions (built-in `tavily` tool)
- `calculate_cost` — totals entry fees + transport + food (built-in `calculator` tool)
- Model: any OpenAI-compatible endpoint (e.g. OpenRouter) via `OpenAIModel`
- Strands' automatic agent loop handles tool round-trips; the prompt pins the
  step order (weather → search → calculate → itinerary).

## Setup

```bash
pip install strands-agents strands-agents-tools requests
cp .env.example .env   # then fill in your keys
```

## Usage

```bash
jupyter notebook travel_planner.ipynb
```

(If Jupyter isn't installed: `python -m pip install notebook`.)

Set `CITY` in the last code cell and run all cells.

### Cell-by-cell walkthrough

| Cell | What it does |
|---|---|
| 1 (code) | Imports, loads `.env`, checks all required keys are set |
| 2 (code) | Loads shared config from `src/constants.py` (adds `src/` to `sys.path`) |
| 3 (code) | Defines the `get_weather` `@tool` and calls it directly for one city |
| 4 (code) | Wires the `OpenAIModel` + `Agent` with the three tools |
| 5 (code) | Runs the agent on `CITY` and prints the one-day itinerary |

Every markdown cell above a code cell explains the step and shows the expected
output, so a reviewer can follow the workflow without running anything.
