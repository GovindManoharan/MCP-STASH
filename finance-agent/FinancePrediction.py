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
from getClaims import fetch_claim_data
from getPriorAuthorizations import fetch_prior_authorizations
from pydantic import BaseModel, Field
from enum import Enum

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


class FinancialPredictor:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    prediction_prompt = PromptTemplate.from_template(
        """"
                    Predict the future stock price movement of a company based on its ticker symbol using available news and financial data tools.

                Utilize the available tools as necessary. DO NOT CALL THE SAME TOOL MORE THAN ONCE FOR THE SAME QUERY.Output should be in in the specified JSON format.
            
                

                # Output Format

                    Generate a JSON response that matches the strucutre of the following python strucutre. 
                    Do ***not*** use triple backticks or any code block markers (e.g., '''json)
                    Only return the raw JSON. Use newline as delimer between entries in arrays with the JSON output for clairy
                        class StockPrediction(BaseModel):
                            company_name: str = Field(..., alias="companyName", description="Name of the company")
                            ticker: str = Field(..., description="Ticker symbol of the company")
                            prediction: str = Field(..., description="Predicted price movement")
                            prediction_reason: str = Field(..., alias="Prediction reason", description="Reason for the prediction")
                            advice: str = Field(..., description="Suggested investment action")
                query: {query} """
    )

    def call_createGraph(self, query: str):
        """Process input and returns output.

        Can use runtime configuration to alter behavior.
        """
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

        graph = create_react_agent(
            llm,
            tools=[self.get_gnews, self.get_finacial_data],
            prompt=self.prediction_prompt.format_prompt(query=query).to_string(),
        )

        result = graph.invoke({"messages": [query]})
        return (
            result["messages"][-1].content
            if result["messages"]
            else "No prediction available."
        )

    @tool
    def get_gnews(query: str):
        """Fetches news articles related to a given query using the GNews API.

        This function is designed to be used as a LangChain tool. It interfaces
        with the `GNewsFetcher` class to retrieve news articles from the
        GNews.io service based on the provided search query.

        The function currently uses default parameters for language ('en'),
        country ('us'), maximum articles (2), and sort order ('publishedAt')
        when calling the underlying `GNewsFetcher.search_articles` method.
        It prints a message to the console indicating the query being processed.

        Args:
            query (str): The search term or topic for which to fetch news articles.
                        For example, 'Tesla stock' or 'AI advancements'.

        Returns:
            Union[dict, None]: A dictionary containing the news articles if the API
            call is successful and articles are found. This dictionary typically
            includes a 'totalArticles' count and a list of 'articles', where
            each article is a dictionary with details like 'title', 'description',
            'url', 'source', etc.
            Returns `None` if the query is empty, if an error occurs during the
            API request (e.g., network issues, invalid API key, GNews API errors),
            or if the response cannot be decoded. The exact structure of the
            returned dictionary and its articles is determined by the GNews API
            and the `GNewsFetcher.search_articles` method.
        """
        print(f"Fetching news articles for query: {query}")
        jsonNews = GNewsFetcher.search_articles(query=query)

        return jsonNews

    @tool
    def get_finacial_data(query: str):
        """Fetches financial data for a given company name or ticker symbol.

        This function is designed to be used as a LangChain tool. It interfaces
        with the `FinancialDataFetcher` class to retrieve financial information
        from an external API (Financial Modeling Prep) based on the provided query.
        The query should be a company's stock ticker symbol (e.g., "AAPL") or
        a company name that can be resolved to a ticker.

        The function prints a message to the console indicating the query being processed.

        Args:
            query (str): The company name or stock ticker symbol for which to
                        fetch financial data. For example, "AAPL" or "Apple Inc.".

        Returns:
            Union[list[dict], None]: A list of dictionaries containing financial data
            (e.g., analyst estimates) for the queried symbol if the API call is
            successful and data is found. Each dictionary in the list typically
            represents a piece of financial information. Returns `None` if the
            query is empty, if an error occurs during the API request (e.g.,
            network issues, invalid API key, symbol not found), or if the
            response cannot be decoded. The exact structure of the dictionaries
            within the list is determined by the `FinancialDataFetcher.search_symbol`
            method and the specific API endpoint it queries.
        """
        print(f"Fetching financial data for query: {query}")

        jsonFinanceData = FinancialDataFetcher.search_symbol(query=query)

        return jsonFinanceData


predictRAG = FinancialPredictor()


@app.post("/predict")
def predict_stock_price(query: str):
    """Endpoint to predict stock price based on company name or ticker."""
    response = predictRAG.call_createGraph(query)

    return response


if __name__ == "__main__":
    # Example usage of the graph directly
    test_query = "AAPL"  # Replace with a ticker you want to test
    print(f"Testing graph with query: {test_query}")
    try:
        prediction_result = predictRAG.call_createGraph(test_query)
        print(f"\nPrediction Result for {test_query}: {prediction_result}")
    except Exception as e:
        print(f"An error occurred during graph execution: {e}")
