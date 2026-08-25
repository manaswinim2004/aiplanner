from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent.agentic_workflow import GraphBuilder
from utils.save_to_document import save_document
from starlette.responses import JSONResponse
import os
import datetime
import re
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set specific origins in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class QueryRequest(BaseModel):
    question: str


def _destination_from_question(question: str) -> str:
    """Extract a destination for deterministic live-data requests."""
    match = re.search(r"\b(?:to|visit|in)\s+([A-Za-z][A-Za-z .'-]*?)(?=\s+(?:for|with|in)\b|[?.!,]|$)", question, re.IGNORECASE)
    return match.group(1).strip() if match else question.strip()


def _run_tool(tool, arguments: dict):
    try:
        return tool.invoke(arguments)
    except Exception as error:
        return f"Live lookup unavailable: {error}"


def _live_trip_data(graph: GraphBuilder, destination: str) -> dict:
    """Call every external live-data tool once for each travel request."""
    weather_tools = graph.weather_tools.weather_tool_list
    place_tools = graph.place_search_tools.place_search_tool_list
    currency_tools = graph.currency_converter_tools.currency_converter_tool_list

    return {
        "current_weather": _run_tool(weather_tools[0], {"city": destination}),
        "weather_forecast": _run_tool(weather_tools[1], {"city": destination}),
        "attractions": _run_tool(place_tools[0], {"place": destination}),
        "restaurants": _run_tool(place_tools[1], {"place": destination}),
        "activities": _run_tool(place_tools[2], {"place": destination}),
        "transportation": _run_tool(place_tools[3], {"place": destination}),
        "usd_to_inr": _run_tool(
            currency_tools[0],
            {"amount": 1.0, "from_currency": "USD", "to_currency": "INR"},
        ),
    }


@app.post("/query")
async def query_travel_agent(query:QueryRequest):
    try:
        print(query)
        graph = GraphBuilder(model_provider="groq")
        destination = _destination_from_question(query.question)
        live_data = _live_trip_data(graph, destination)
        live_context = "\n\n".join(
            f"{name}: {str(value)[:3500]}" for name, value in live_data.items()
        )
        response = graph.llm.invoke([
            graph.system_prompt,
            HumanMessage(content=(
                f"Travel request: {query.question}\n\n"
                f"<live_data destination=\"{destination}\">\n{live_context}\n</live_data>\n\n"
                "Create the travel plan from this live data. Do not invent current weather, "
                "places, transport, or exchange rates when a lookup failed."
            )),
        ])
        final_output = response.content

        if not final_output or not str(final_output).strip():
            raise RuntimeError("The model returned an empty final response.")
        
        return {"answer": final_output}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
