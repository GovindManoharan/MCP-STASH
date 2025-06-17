import requests
import json
import os  # Added for environment variable access


class GNewsFetcher:
    """
    A class to fetch news articles from the GNews API.
    """

    GNEWS_BASE_URL = "https://gnews.io/api/v4"

    def __init__(self, gnews_api_key):
        """
        Initializes the GNewsFetcher with a GNews API key.

        Args:
            gnews_api_key (str): Your API key for GNews.io.
        """
        if not gnews_api_key:
            raise ValueError("GNews API key cannot be empty.")
        self.gnews_api_key = gnews_api_key

    @staticmethod
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

        api_key =  os.getenv("GNEWS_API_KEY")

        endpoint = f"{GNewsFetcher.GNEWS_BASE_URL}/search"
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
    # Attempt to get the API key from an environment variable
    api_key = "bad202cd56a6df3fbd5d8222a2fe9ce2"

    if not api_key:
        print("Error: GNEWS_API_KEY environment variable not set.")
        print("Please set it before running the script.")
        print("Example: export GNEWS_API_KEY='your_actual_api_key'")
    else:
        print(
            f"Using GNews API Key: {'*' * (len(api_key) - 4) + api_key[-4:] if len(api_key) > 4 else '****'}"
        )  # Mask part of the key for display
        fetcher = GNewsFetcher(gnews_api_key=api_key)

        # Test case 1: Basic search
        print("\n--- Test Case 1: Basic Search ---")
        query1 = "artificial intelligence"
        print(f"Searching for: '{query1}'")
        articles1 = fetcher.search_articles(query=query1, max_articles=3)
        if articles1 and "articles" in articles1:
            print(
                f"Found {articles1.get('totalArticles', 0)} articles. Displaying up to 3."
            )
            for i, article in enumerate(articles1["articles"]):
                print(
                    f"  {i+1}. {article.get('title')} ({article.get('source', {}).get('name')}) - {article.get('url')}"
                )
        else:
            print("No articles found or an error occurred.")

        # Test case 2: Search with different parameters
        print("\n--- Test Case 2: Search in German (de) for 'Technologie' ---")
        query2 = "Technologie"
        print(
            f"Searching for: '{query2}' in German, sorted by relevance, max 2 articles"
        )
        articles2 = fetcher.search_articles(
            query=query2, lang="de", country="de", max_articles=2, sort_by="relevance"
        )
        if articles2 and "articles" in articles2:
            print(
                f"Found {articles2.get('totalArticles', 0)} articles. Displaying up to 2."
            )
            for i, article in enumerate(articles2["articles"]):
                print(
                    f"  {i+1}. {article.get('title')} ({article.get('source', {}).get('name')}) - {article.get('url')}"
                )
        else:
            print("No articles found or an error occurred.")

        # Test case 3: Empty query (should be handled by the method)
        print("\n--- Test Case 3: Empty Query ---")
        articles3 = fetcher.search_articles(query="")
        if articles3 is None:
            print("Test for empty query passed (method returned None as expected).")
        else:
            print("Test for empty query failed.")

        # Test case 4: Invalid API key (simulated by creating a new fetcher with a bad key)
        # Note: This will likely result in an HTTP 401 Unauthorized error from the API.
        print("\n--- Test Case 4: Invalid API Key (Simulated) ---")
        bad_fetcher = GNewsFetcher(gnews_api_key="INVALID_KEY_FOR_TESTING")
        articles4 = bad_fetcher.search_articles(query="test")
        if articles4 is None:
            print(
                "Test for invalid API key likely resulted in an error as expected (method returned None)."
            )
        else:
            print(
                "Test for invalid API key might not have behaved as expected if articles were returned."
            )
