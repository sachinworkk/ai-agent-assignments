"""Basic Gemini chatbot — sanity check before building the weather agent.

Loads GEMINI_API_KEY from .env and sends a simple "Hello, world!" prompt
to the model to verify the SDK + API key are working.
"""

import os

from dotenv import load_dotenv
from google import genai

from constants import ERR_MISSING_GEMINI_KEY, MODEL

# Load .env from this directory (GEMINI_API_KEY, OPENWEATHER_API_KEY)
load_dotenv()

if not os.getenv("GEMINI_API_KEY"):
    raise SystemExit(ERR_MISSING_GEMINI_KEY)

client = genai.Client()

print(f"--- Sending test prompt to {MODEL} ---")
response = client.models.generate_content(
    model=MODEL,
    contents="Hello, world! Reply with one short sentence to confirm you are working.",
)

print("--- Response ---")
print(response.text)
