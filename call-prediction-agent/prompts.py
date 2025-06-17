from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate



client = Client()

CALL_PREDICTION_PROMPT = """
            Analyze the claims and prior authorization details for a given user_id {user_id} using available tools to predict the 
            potential reasons for a user call to a pharmacy benefit manager call center.
            - Extract and evaluate claims and prior authorization information for the provided user_id.
            - Formulate a prediction on the potential reasons the user might be calling. The prediction should be a list of strings.
            - Your prediction list **MUST** contain one or both of the following strings: 'CLAIMS' or 'PRIOR_AUTHORIZATION'.
            - Justify the prediction based on the user’s recent claims or authorization history.
            - Provide any relevant supporting information related to the prediction, such as claim or authorization IDs.
            - Think step by step and arrive at a prediction. 

            # Steps

            1. **Access Data**: Retrieve claims and prior authorization details using the user's ID.
            2. **Analyze History**: Examine the timeline and status of claims and prior authorizations to identify recent or significant actions.
            3. **Predict Call Reason**: Based on the analysis, predict the likely reason for the user's call. Consider the recency and significance of events.
            4. **Justify Prediction**: Provide reasoning for the prediction based on the data analyzed.
            5. **Provide Supporting Info**: Include any specific claim or authorization IDs relevant to the prediction.

            # Output Format

            Generate a JSON response that matches the strucutre of the following python strucutre. 
            Do ***not*** use triple backticks or any code block markers (e.g., '''json)
            Only return the raw JSON. Use newline as delimer between entries in arrays with the JSON output for clairy

            class CallPredictionResponse(BaseModel):
                user_id: str = Field(..., description="User identifier")
                prediction: list[str] = Field(..., description="A list of predicted reasons for the user's call (e.g., ['CLAIMS'], ['PRIOR_AUTHORIZATION'], ['CLAIMS', 'PRIOR_AUTHORIZATION'])")
                prediction_reason: str = Field(..., alias="prediction reason", description="Justification for the predicted reasons")
                supporting_info: str = Field(..., alias="Supporting info", description="Relevant supporting information like claim or authorization IDs")


            (Note: Real examples should contain actual claim or authorization IDs, and explanations should be based on real claim data.)"""

prompt = ChatPromptTemplate([
("system", CALL_PREDICTION_PROMPT),
("user", "{user_id}"),
])

# Push the prompt

# client.push_prompt("mcp-demo-prompt", object=prompt)