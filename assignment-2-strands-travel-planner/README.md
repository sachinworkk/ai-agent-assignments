# Strands Travel Planner (Assignment 2)

AI agent built with [Strands Agents](https://github.com/strands-agents/sdk-python)
that plans a one-day trip for a city: checks current weather, finds 3 popular
attractions, estimates total visit cost, and writes a one-day itinerary.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in your keys
```

## Run

```bash
python src/main.py "Kathmandu"
```

## Tools used by the agent

- `get_weather` — current weather via OpenWeather
- `search_attractions` — web search for 3 popular attractions
- `calculate_cost` — totals entry fees + transport + food
