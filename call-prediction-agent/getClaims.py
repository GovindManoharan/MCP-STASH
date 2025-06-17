import requests
import json


def fetch_claim_data(user_id: str):
    """
    Fetches claim data for a specific user and claim ID from a local endpoint.

    Args:
        user_id (str): The ID of the user.
        claim_id (str): The ID of the claim.

    Returns:
        dict: A dictionary containing the claim data if successful, None otherwise.
    """
    if not user_id:
        print("Error: User ID cannot be empty.")
        return None

    base_url = "http://localhost:8000/claims_service/claims"
    endpoint = f"{base_url}/{user_id}"

    print(f"Fetching claim data from: {endpoint}")

    try:
        response = requests.get(endpoint, timeout=10)  # Added a timeout
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
        return response.json()  # Returns the JSON response as a Python dict
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
    print("--- Test Case 1: Fetching a specific claim ---")
    test_user_id = "U123456789"
    test_claim_id = "CLM20250522002"

    claim_data = fetch_claim_data(user_id=test_user_id, claim_id=test_claim_id)

    if claim_data:
        print("\nSuccessfully fetched claim data:")
        # Assuming the claim data is a dictionary, you can print it or access its keys
        # For example, if you expect a 'status' and 'details' key:
        # print(f"  Claim Status: {claim_data.get('status')}")
        # print(f"  Details: {claim_data.get('details')}")
        # For now, let's just print the whole dictionary
        print(json.dumps(claim_data, indent=2))
    else:
        print(
            f"\nFailed to fetch claim data for user '{test_user_id}', claim '{test_claim_id}'."
        )

    print("\n--- Test Case 2: Empty User ID ---")
    fetch_claim_data(user_id="", claim_id="claimXYZ")

    print("\n--- Test Case 3: Empty Claim ID ---")
    fetch_claim_data(user_id="user789", claim_id="")

    # To run this example, you would need a local server running at http://localhost:8000
    # that responds to GET requests at /claims/{user_id}/{claim_id} with JSON data.
    # For example, a simple Flask or FastAPI server.
