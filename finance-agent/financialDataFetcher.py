import requests
import json
import os

from dotenv import load_dotenv


load_dotenv()

class FinancialDataFetcher:
    """
    A class to fetch financial data from the Financial Modeling Prep API.
    """
    BASE_URL = "https://financialmodelingprep.com/stable/analyst-estimates" # Using v3 as it's common, adjust if needed

    def __init__(self, api_key):
        """
        Initializes the FinancialDataFetcher with an API key.

        Args:
            api_key (str): Your API key for Financial Modeling Prep.
        """
        if not api_key:
            raise ValueError("API key cannot be empty.")
        self.api_key = api_key
   
    @staticmethod
    def search_symbol(query):
        """
        Searches for a symbol based on a query.

        Args:
            query (str): The search term (e.g., 'AAPL', 'Microsoft').

        Returns:
            list: A list of dictionaries containing symbol information if successful,
                  None otherwise.
        """
        if not query:
            print("Error: Search query cannot be empty.")
            return None
        my_api_key = os.getenv("FINANCIAL_MODELING_PREP_API_KEY")
        endpoint = "https://financialmodelingprep.com/stable/analyst-estimates"
        params = {
            "symbol": query,
            "period": "annual",  # Assuming 'annual' is the default period, adjust if needed
            "apikey": my_api_key
        }

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
            print(f"Response status code: {response.content}")  # Debugging line
            return response.json()  # Returns the JSON response as a Python list/dict
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print(f"Response content: {response.content}")
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"An unexpected error occurred with the request: {req_err}")
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from response.")
            print(f"Response content: {response.content}")
        return None

