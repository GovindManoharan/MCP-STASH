from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from getClaims import fetch_claim_data
from getPriorAuthorizations import fetch_prior_authorizations
from langchain_core.prompts import ChatPromptTemplate
from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
from prompts import CALL_PREDICTION_PROMPT
from langsmith import Client
from langsmith import traceable, tracing_context

# Load environment variables from .env file
# This should be called as early as possible in your application
load_dotenv()

app = FastAPI()




class CallPredictionResponse(BaseModel):
    user_id: str = Field(..., description="User identifier")
    prediction: list[str] = Field(
        ..., description="A list of predicted reasons for the user's call"
    )
    prediction_reason: str = Field(
        ..., alias="prediction reason", description="Justification for the prediction"
    )
    supporting_info: str = Field(
        ...,
        alias="Supporting info",
        description="Relevant supporting information like claim or authorization IDs",
    )


class CallPredictor:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


    
    
    @traceable(run_type="chain", name="Call Center ReAct Agent", project_name="Promblem-first-ai-demo")
    def predict_with_llm(self, user_id: str):
        client = Client()
        prompt = client.pull_prompt("mcp-demo-prompt")
        graph = create_react_agent(
            self.llm,
            tools=[self.get_prior_authorizations, self.get_claims],
            prompt= prompt.format(user_id=user_id),
        )


        result = graph.invoke({"messages": user_id})
        print(result["messages"][-1].content)
        return (
            result["messages"][-1].content
            if result["messages"]
            else "No prediction available."
        )

    @tool
    def get_prior_authorizations(query: str):
        """Fetches a list of prior authorizations for a given user_id.

        This function is designed to be used as a LangChain tool. It interfaces
        with the `fetch_prior_authorizations` function to retrieve a list of
        prior authorization records associated with a specific user_id from a
        predefined local service endpoint.

        The function prints a message to the console indicating the user_id
        for which prior authorizations are being fetched.

        Args:
            query (str): The user_id for which to fetch prior authorization data.
                        For example, "U987654321".

        Returns:
            Union[list[dict], None]: A list of dictionaries, where each dictionary
            represents a prior authorization record, if the API call is successful
            and data is found. Returns `None` if the user_id (query) is empty,
            if an error occurs during the API request (e.g., network issues,
            server error), or if the response cannot be decoded. The structure
            of the dictionaries within the list is determined by the
            `fetch_prior_authorizations` function and the API it queries.
        """
        print(f"Fetching prior authorizations for user_id: {query}")
        prior_authorizations = fetch_prior_authorizations(user_id=query)
        return prior_authorizations

    @tool
    def get_claims(query: str):
        """Fetches claim data for a specific user_id.

        This function is designed to be used as a LangChain tool. It interfaces
        with the `fetch_claim_data` function to retrieve claim information
        associated with a specific user_id from a predefined local service endpoint.
        Note: The underlying `fetch_claim_data` function in `getClaims.py` is
        currently structured to fetch claims based on `user_id` only, even though
        it might have originally been intended for a specific claim ID as well.

        The function prints a message to the console indicating the user_id
        for which claim data is being fetched.

        Args:
            query (str): The user_id for which to fetch claim data.
                        For example, "U123456789".

        Returns:
            Union[dict, None]: A dictionary containing the claim data if successful,
            or a list of claims if the endpoint returns multiple. Returns `None` if
            the user_id (query) is empty, if an error occurs during the API request
            (e.g., network issues, server error), or if the response cannot be
            decoded. The structure of the returned data is determined by the
            `fetch_claim_data` function and the API it queries.
        """
        print(f"Fetching claims for user_id: {query}")
        claims = fetch_claim_data(user_id=query)
        return claims


predictRAG = CallPredictor()


@app.post("/predict")
async def predict_call_reason(user_id: str):
    """Endpoint to predict stock price based on company name or ticker."""
    print(f"Received user_id: {user_id}")
    response = predictRAG.predict_with_llm(user_id=user_id)

    return response


if __name__ == "__main__":
    print("Testing CallPredictor class directly...")

    # Ensure your .env file has OPENAI_API_KEY set, or it's in your environment
    # Also, the tools will try to connect to http://localhost:8000
    # You might want to mock these external calls for isolated testing.

    predictor = CallPredictor()
    test_user_id = "U123456789"  # Replace with a test user_id

    print(f"\nAttempting to predict call reason for user_id: {test_user_id}")
    try:
        prediction = predictor.predict_with_llm(user_id=test_user_id)
        print("\nPrediction Result:")
        print(prediction)
    except Exception as e:
        print(f"\nAn error occurred during prediction: {e}")
        print(
            "This might be due to API key issues, network issues, or the agent/prompt configuration."
        )
