import requests
import json
from mcp.server.fastmcp import FastMCP
import os 
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("Finance MCP Server")


@mcp.tool()
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
        "apikey": my_api_key,
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


@mcp.tool()
def search_articles(
    query, lang="en", country="us", max_articles=2, sort_by="publishedAt"
):
    """
    Searches for articles on GNews API based on a query.

    Args:
        query (str): The search term (e.g., 'Tesla', 'AI development').
        lang (str, optional): Language of the news (e.g., 'en', 'es', 'fr'). Defaults to "en".
        country (str, optional): Country for the news (e.g., 'us', 'gb', 'ca'). Defaults to "us".
        max_articles (int, optional): The maximum number of articles to return (1-100). Defaults to 10.
        sort_by (str, optional): Sort order ('publishedAt' or 'relevance'). Defaults to "publishedAt".

    Returns:
        dict: A dictionary containing the news articles if successful, None otherwise.
              The structure includes 'totalArticles' and a list of 'articles'.
    """
    if not query:
        print("Error: GNews search query cannot be empty.")
        return None

    api_key =os.getenv("GNEWS_API_KEY")
    GNEWS_BASE_URL = "https://gnews.io/api/v4"

    endpoint = f"{GNEWS_BASE_URL}/search"
    params = {
        "q": query,
        "lang": lang,
        "country": country,
        "max": max_articles,
        "sortby": sort_by,
        "apikey": api_key,
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
        return response.json()  # Returns the JSON response as a Python dict
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.content}")
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
        requests.exceptions.RequestException,
    ) as req_err:
        print(f"A network or request error occurred: {req_err}")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from response.")
        print(f"Response content: {response.content}")
    return None


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")
