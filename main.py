from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent.agentic_workflow import GraphBuilder
from starlette.responses import JSONResponse
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


@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    try:
        graph_builder = GraphBuilder(model_provider="groq")
        graph = graph_builder.build_graph()

        # Let the LangGraph agent autonomously decide which tools to call
        response = graph.invoke({
            "messages": [HumanMessage(content=query.question)]
        })

        # The last message in the state contains the final answer
        final_output = response["messages"][-1].content

        if not final_output or not str(final_output).strip():
            raise RuntimeError("The model returned an empty final response.")

        return {"answer": final_output}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
