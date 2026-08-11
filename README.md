# AI Travel Planner

AI Travel Planner is an agentic trip-planning application that combines `FastAPI`, `Streamlit`, `LangGraph`, and tool-augmented LLM workflows to generate detailed travel itineraries with live supporting data.

The project is built around a travel assistant that can plan end-to-end trips, suggest attractions and restaurants, estimate hotel and daily budgets, surface weather conditions, and handle currency conversion for international travel.

## Why This Project

Travel planning usually requires jumping across multiple apps for discovery, budgeting, weather checks, and local logistics. This project brings those steps into one agent workflow by giving an LLM access to specialized tools and a structured reasoning graph.

## Key Features

- Generates detailed day-by-day travel itineraries in Markdown
- Recommends attractions, restaurants, activities, and transportation options
- Pulls weather and forecast data for destination-aware planning
- Estimates total trip cost and per-day budget using calculator tools
- Supports currency conversion for international travel scenarios
- Uses fallback search behavior for place discovery when primary lookup fails
- Exposes backend API with `FastAPI`
- Provides simple chat-style frontend with `Streamlit`
- Builds workflow as a reusable `LangGraph` agent graph

## Architecture

The application has two layers:

1. `Streamlit` frontend
   Collects user trip requests and displays the generated plan.

2. `FastAPI` backend
   Accepts user queries, builds the agent graph, invokes the LLM workflow, and returns the final answer.

Inside the backend, the `GraphBuilder` creates an agent loop using `LangGraph`:

- `agent` node:
  Sends the user request plus system prompt to the LLM.
- `tools` node:
  Executes external tools when the model decides they are needed.
- conditional routing:
  Continues tool use until the model has enough information to produce the final itinerary.

## Tools Used By The Agent

- Weather tools:
  Current weather and short forecast via OpenWeatherMap
- Place search tools:
  Attractions, restaurants, activities, and transportation lookup via Google Places with Tavily fallback
- Expense tools:
  Hotel cost estimation, total expense calculation, and daily budget calculation
- Currency conversion tool:
  Exchange-rate-based amount conversion

## Tech Stack

- Python 3.10+
- FastAPI
- Streamlit
- LangChain
- LangGraph
- Groq / OpenAI chat models
- Google Places
- Tavily Search
- OpenWeatherMap API
- ExchangeRate API

## Project Structure

```text
aiplanner/
├── agent/                   # LangGraph workflow builder
├── config/                  # Model provider configuration
├── prompt_library/          # System prompt for travel planning behavior
├── tools/                   # LangChain tool wrappers
├── utils/                   # API clients and helper utilities
├── main.py                  # FastAPI backend entrypoint
├── streamlit_app.py         # Streamlit frontend entrypoint
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Getting Started

### 1. Clone And Enter Project

```bash
git clone <your-repo-url>
cd aiplanner
```

### 2. Create Virtual Environment

```bash
python -m venv env
```

Activate it:

```bash
# Windows
env\Scripts\activate

# macOS / Linux
source env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
OPENAI_API_KEY=""
GROQ_API_KEY=""
GPLACES_API_KEY=""
OPENWEATHERMAP_API_KEY=""
EXCHANGE_RATE_API_KEY=""
TAVILY_API_KEY=""
```

Notes:

- `GROQ_API_KEY` is needed for default model execution in current backend flow
- `OPENAI_API_KEY` is optional unless you switch provider to OpenAI
- Google Places and weather keys are needed for richer itinerary generation
- Tavily improves resilience when Google place lookup fails

### 5. Run Backend

```bash
uvicorn main:app --reload --port 8000
```

Backend endpoint:

```text
POST /query
```

Request body:

```json
{
  "question": "Plan a 5-day trip to Goa with budget details"
}
```

### 6. Run Frontend

```bash
streamlit run streamlit_app.py
```

## Example Use Cases

- Plan a 3-day solo trip to Jaipur with hotel and food budget
- Create a family itinerary for Goa with beaches, restaurants, and weather details
- Estimate cost of a Europe trip and convert budget into local currency
- Explore offbeat destinations around a city instead of only standard tourist spots

## Resume-Ready Project Summary

Built an agentic AI travel planner using `FastAPI`, `Streamlit`, `LangGraph`, and `LangChain`, integrating weather, place discovery, budgeting, and currency-conversion tools to generate detailed trip itineraries from natural-language prompts.

## Current Limitations

- Frontend currently points to a deployed backend URL instead of local `localhost`
- Some API key names in repository templates may need cleanup for consistency
- Output quality depends on external API availability and LLM/tool responses
- Travel recommendations should still be manually verified before booking

## Future Improvements

- User authentication and saved trip history
- PDF or DOCX itinerary export
- Maps and route visualization
- Flight and hotel booking integrations
- Caching for repeated destination queries
- Local/backend environment switching from frontend config

## License

This project is for learning, experimentation, and portfolio use unless you add a separate license file.
