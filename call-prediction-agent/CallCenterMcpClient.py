from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from getClaims import fetch_claim_data
from getPriorAuthorizations import fetch_prior_authorizations
from langchain.prompts import PromptTemplate
from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
from prompts import CALL_PREDICTION_PROMPT
from mcp_use import MCPAgent, MCPClient
import uuid
from langsmith import traceable


# Load environment variables from .env file
# This should be called as early as possible in your application
load_dotenv()

app = FastAPI()




class CallPredictor:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    @traceable(run_type="chain", name="Call Center MCP Agent", project_name="Promblem-first-ai-demo")
    async def predict_with_llm(self, user_id: str):

        # Create MCPClient from configuration dictionary
        client = MCPClient.from_config_file(os.path.join("/Users/gman/Documents/Problem-First/mcp-servers/CallCenterMcpServer.json"))
        conversation_id = uuid.uuid4()
        # Create agent with the client
        graph = MCPAgent(llm=self.llm, client=client, max_steps=30)

        result = await graph.run(user_id, max_steps=10)

        return result


predictRAG = CallPredictor()


@app.post("/predict")
async def predict_call_reason(query: str):
    """End point to predict the reason for a call based on query."""
    print(f"Received user_id: {query}")
    response = await predictRAG.predict_with_llm(user_id=query)

    return response
