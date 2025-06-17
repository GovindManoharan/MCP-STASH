"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, TypedDict

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from gnewsFetcher import GNewsFetcher
from financialDataFetcher import FinancialDataFetcher
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain.prompts import PromptTemplate
from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from enum import Enum
from mcp_use import MCPAgent, MCPClient
import os
from fastmcp import FastMCP,Client
from langsmith import traceable
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools

# Load environment variables from .env file
load_dotenv()  # This will load variables from .env into your environment


app = FastAPI()


class StockPrediction(BaseModel):
    company_name: str = Field(
        ..., alias="companyName", description="Name of the company"
    )
    ticker: str = Field(..., description="Ticker symbol of the company")
    prediction: str = Field(..., description="Predicted price movement")
    prediction_reason: str = Field(
        ..., alias="Prediction reason", description="Reason for the prediction"
    )
    advice: str = Field(..., description="Suggested investment action")


class Configuration(TypedDict):
    """Configurable parameters for the agent.

    Set these when creating assistants OR when invoking the graph.
    See: https://langchain-ai.github.io/langgraph/cloud/how-tos/configuration_cloud/
    """

    my_configurable_param: str


@dataclass
class State:
    """Input state for the agent.

    Defines the initial structure of incoming data.
    See: https://langchain-ai.github.io/langgraph/concepts/low_level/#state
    """

    messages: list[str]

mcp = FastMCP("Finance MCP Server")


server_params = StdioServerParameters(
    command="python",
    # Make sure to update to the full absolute path to your math_server.py file
    args=["/Users/gman/Documents/Problem-First/dummy-data/financeMCPServer.py"],
)



class FinancialPredictor:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


    @traceable(run_type="chain", name="Finance MCP Agent", project_name="Promblem-first-ai-demo")
    async def call_createGraph(self, query: str):
        """Process input and returns output.

        Can use runtime configuration to alter behavior.
        """
        server_params = StdioServerParameters(
            command="python",
            # Make sure to update to the full absolute path to your math_server.py file
            args=[
                "/Users/gman/Documents/Problem-First/dummy-data/financeMCPServer.py"
            ],
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()

                # Get tools
                tools = await load_mcp_tools(session)

                # Create and run the agent
                agent = create_react_agent(self.llm, tools)
                agent_response = await agent.ainvoke(
                    {"messages": query},
                )
                return agent_response.get('messages')[-1].content

   
predictRAG = FinancialPredictor()

@app.post("/predict")
async def predict_stock_price(query: str):
    """Endpoint to predict stock price based on company name or ticker."""
    response = await predictRAG.call_createGraph(query)

    return response

