import requests
import json


def fetch_prior_authorizations(user_id: str):
    """
    Fetches a list of prior authorizations for a specific user ID from a local endpoint.

    Args:
        user_id (str): The ID of the user.

    Returns:
        list: A list of dictionaries containing prior authorization data if successful, None otherwise.
    """
    if not user_id:
        print("Error: User ID cannot be empty.")
        return None

    base_url = "http://localhost:8000/pa_service/pas"
    endpoint = f"{base_url}/{user_id}"

    print(f"Fetching prior authorizations from: {endpoint}")

    try:
        response = requests.get(endpoint, timeout=10)  # Added a timeout
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
        return response.json()  # Returns the JSON response as a Python list of dicts
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(
            f"Response content: {response.content if 'response' in locals() else 'N/A'}"
        )
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
        print(f"Failed to connect to {endpoint}. Ensure the server is running.")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected error occurred with the request: {req_err}")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from response.")
        print(
            f"Response content: {response.content if 'response' in locals() else 'N/A'}"
        )
    return None


if __name__ == "__main__":
    print("--- Test Case 1: Fetching prior authorizations for a user ---")
    test_user_id_pa = "U123456789"

    pa_data = fetch_prior_authorizations(user_id=test_user_id_pa)

    if pa_data:
        print("\nSuccessfully fetched prior authorization data:")
        # Assuming pa_data is a list of dictionaries
        print(json.dumps(pa_data, indent=2))
        # Example of accessing data if it's a list of PAs
        # for i, pa_item in enumerate(pa_data):
        #     print(f"  PA {i+1}: ID - {pa_item.get('pa_id')}, Status - {pa_item.get('status')}")
    else:
        print(f"\nFailed to fetch prior authorizations for user '{test_user_id_pa}'.")

    print("\n--- Test Case 2: Empty User ID ---")
    fetch_prior_authorizations(user_id="")

    # To run this example, you would need a local server running at http://localhost:8000
    # that responds to GET requests at /pa_service/pas/{user_id} with JSON data (likely a list).
