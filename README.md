# AI Agent Assignments

All three assignments in one repository. Each folder is a standalone project with its own README and setup instructions.

| # | Assignment | Folder | Tech |
|---|------------|--------|------|
| 1 | Weather Agent: sequential OpenWeather tool calls + average temperature | [assignment-1-weather-agent-gemini](assignment-1-weather-agent-gemini/) | Gemini SDK |
| 2 | Travel Planner Agent with weather, search and calculator tools | [assignment-2-strands-travel-planner](assignment-2-strands-travel-planner/) | Strands Agents |
| 3 | Travel Planner Chatbot (interactive one-day trip planner) | [assignment-3-strands-travel-chatbot](assignment-3-strands-travel-chatbot/) | Strands Agents + Gradio |

## Running a project

1. **Clone and enter the repo**

   ```bash
   git clone <repo-url>
   cd ai-agent-assignments
   ```

2. **Pick an assignment and enter its folder** (each folder is standalone —
   you don't need to install anything from the other assignments):

   ```bash
   cd assignment-2-strands-travel-planner
   ```

3. **Install dependencies** into a virtual environment (from the repo root —
   one master `requirements.txt` covers all three assignments):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Add your API keys**

   ```bash
   cp .env.example .env   # then fill in the keys
   ```

   Every assignment needs:

   - `OPENWEATHER_API_KEY` — https://openweathermap.org/api (free; new keys take
     ~10 min to a couple of hours to activate — a 401 right after signup is normal)
   - `TAVILY_API_KEY` — https://tavily.com (free) — assignments 2 and 3
   - An LLM key: `GEMINI_API_KEY` for assignment 1 (https://aistudio.google.com),
     `OPENROUTER_API_KEY` (https://openrouter.ai) for assignments 2 and 3

5. **Run it** — assignments 1 and 2 are Jupyter notebooks, assignment 3 is a
   Gradio app. Either way, follow the README inside the folder for the details:

   ```bash
   jupyter notebook assignment-1-weather-agent-gemini/weather_agent.ipynb     # assignment 1
   jupyter notebook assignment-2-strands-travel-planner/travel_planner.ipynb  # assignment 2
   python assignment-3-strands-travel-chatbot/src/app.py                      # assignment 3 → http://127.0.0.1:7860
   ```

   (If Jupyter isn't installed: `python -m pip install notebook`.)
