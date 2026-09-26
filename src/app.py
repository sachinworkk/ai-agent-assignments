"""Assignment 3: Strands Travel Planner Chatbot.

Interactive Gradio chatbot that plans a one-day trip for any city:
1. Weather tool  -> current weather (OpenWeather)
2. Search tool   -> 3 popular attractions (Tavily)
3. Calculator    -> total estimated cost (built-in strands_tools.calculator)
4. Agent combines everything into a one-day itinerary, delivered in chat.

Model provider: OpenRouter (OpenAI-compatible) using gpt-oss-20b.
"""

import os
import re

import gradio as gr
import requests
from dotenv import load_dotenv

from constants import (
    CHAT_ERROR,
    GREETING_MAX_WORDS,
    GREETING_PATTERNS,
    OPENWEATHER_URL,
    SYSTEM_PROMPT,
    UI_DESCRIPTION,
    UI_EXAMPLES,
    UI_TITLE,
    WEATHER_NOT_FOUND,
    WEATHER_SUMMARY,
)
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
        OPENWEATHER_URL,
        params={"q": city, "units": "metric", "appid": OPENWEATHER_API_KEY},
        timeout=15,
    )
    if resp.status_code == 404:
        return WEATHER_NOT_FOUND.format(city=city)
    resp.raise_for_status()
    data = resp.json()
    temp = data["main"]["temp"]
    feels = data["main"]["feels_like"]
    desc = data["weather"][0]["description"]
    name = data["name"]
    return WEATHER_SUMMARY.format(name=name, temp=temp, feels=feels, desc=desc)


# ---------- Agent ----------

MODEL = OpenAIModel(
    client_args={"api_key": LLM_API_KEY, "base_url": LLM_BASE_URL},
    model_id=LLM_MODEL,
    params={"temperature": 0.4, "reasoning_effort": "low"},
)

agent = Agent(
    model=MODEL,
    tools=[get_weather, tavily, calculator],
    system_prompt=SYSTEM_PROMPT,
)


def small_talk_reply(message: str) -> str | None:
    """Return a canned reply for greetings/small talk, or None to pass to the agent.

    Greeting phrases must match as whole words ("hi", not the "hi" in
    "this"), and only in short messages. Off-topic questions are NOT
    filtered here — the agent's system prompt (TOPIC GUARDRAIL) decides
    what is on-topic and refuses everything else.
    """
    text = re.sub(r"[^a-z ]", " ", message.lower())
    words = text.split()
    if len(words) > GREETING_MAX_WORDS:
        return None
    normalized = " ".join(words)
    return next(
        (reply for phrase, reply in GREETING_PATTERNS if f" {phrase} " in f" {normalized} "),
        None,
    )


def chat(message: str, history: list) -> str:
    """Gradio chat handler: routes every message through the Strands agent.

    The agent's conversation is persisted per browser session so follow-ups
    ("make it cheaper") keep context.
    """
    del history  # Gradio supplies it; the Strands agent keeps its own context.
    try:
        reply = small_talk_reply(message)
        if reply is not None:
            return reply
        return str(agent(message))
    except Exception as exc:  # noqa: BLE001 - user-facing error handling
        return CHAT_ERROR.format(exc=exc)


demo = gr.ChatInterface(
    fn=chat,
    title=UI_TITLE,
    description=UI_DESCRIPTION,
    examples=UI_EXAMPLES,
)


if __name__ == "__main__":
    demo.launch()
