from fastapi import FastAPI

# Import the app instances from your existing modules
# It's good practice to alias them to avoid naming conflicts
# and to make their origin clear.
from claims import app as claims_service_app
from priorAuth import app as prior_auth_service_app

# Create the main FastAPI application
app = FastAPI(title="PBM Services API")

# Mount the claims service application
# All routes from claims.py (e.g., /claims/{user_id})
# will now be accessible under /api/claims_service/claims/{user_id}
app.mount("/claims_service", claims_service_app)

# Mount the prior authorization service application
# All routes from priorAuth.py (e.g., /pa_requests/{user_id})
# will now be accessible under /api/pa_service/pa_requests/{user_id}
app.mount("/pa_service", prior_auth_service_app)


@app.get("/v1.0")
async def read_root():
    return {
        "message": "Welcome to the PBM Services API. Navigate to /docs for API documentation."
    }


# To run this main application, navigate to your project's root directory in the terminal
# (the one containing the 'src' folder) and use a command like:
# uvicorn src.main:app --reload
