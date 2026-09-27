# Assignment 3: Strands Travel Planner Chatbot

Interactive Gradio chatbot that plans a one-day trip for any city.

## What it does
1. **Weather tool** — current weather via OpenWeather.
2. **Search tool** — 3 popular attractions via Tavily.
3. **Calculator tool** — total estimated per-person cost (USD).
4. Replies in chat with a one-day itinerary (weather, morning/afternoon/evening schedule, cost breakdown).

Follow-ups work: ask it to make the trip cheaper or swap a city mid-conversation.

## Model
Strands Agents with OpenRouter (OpenAI-compatible endpoint), default model `openai/gpt-oss-20b`.

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env   # then fill in the keys (shared, at the repo root)
python src/app.py
```

## Keys needed (`.env`)
- `OPENWEATHER_API_KEY` — https://openweathermap.org/api (free)
- `LLM_API_KEY` / `OPENROUTER_API_KEY` — https://openrouter.ai
- `TAVILY_API_KEY` — https://tavily.com (free)
- `LLM_BASE_URL` = `https://openrouter.ai/api/v1`, `LLM_MODEL` = `openai/gpt-oss-20b`

Then open http://127.0.0.1:7860 in your browser.
