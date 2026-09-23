"""Basic Gemini chatbot — sanity check before building the weather agent.

Loads GEMINI_API_KEY from .env and sends a simple "Hello, world!" prompt
to the model to verify the SDK + API key are working.
"""

import os

from dotenv import load_dotenv
from google import genai

MODEL = "gemini-flash-lite-latest"  # lite alias = highest free-tier rate limit

# Load .env from this directory (GEMINI_API_KEY, OPENWEATHER_API_KEY)
load_dotenv()

if not os.getenv("GEMINI_API_KEY"):
    raise SystemExit("GEMINI_API_KEY missing — copy .env.example to .env and fill it in.")

client = genai.Client()

print(f"--- Sending test prompt to {MODEL} ---")
response = client.models.generate_content(
    model=MODEL,
    contents="Hello, world! Reply with one short sentence to confirm you are working.",
)

print("--- Response ---")
print(response.text)
