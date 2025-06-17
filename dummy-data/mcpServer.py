from fastapi import FastAPI, HTTPException, Response
from motor.motor_asyncio import AsyncIOMotorClient
from bson.json_util import dumps
import os
from fastapi_mcp import FastApiMCP

api_app = FastAPI()
# mcp_app = FastAPI()


# MongoDB connection settings
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "pbm_db"
COLLECTION_NAME = "claims"
PA_COLLECTION_NAME = "pa_requests"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
claims_collection = db[COLLECTION_NAME]
pa_collection = db[PA_COLLECTION_NAME]


@api_app.get("/claims/{user_id}", operation_id="get_all_claims")
async def get_all_claims(user_id: str):
    doc = await claims_collection.find_one({"user_id": user_id})
    if not doc:
        raise HTTPException(status_code=404, detail="No claims found for this user")
    return Response(content=dumps(doc), media_type="application/json")


@api_app.get("/claims/{user_id}/{claim_id}", operation_id="get_claim_by_id")
async def get_claim_by_id(user_id: str, claim_id: str):
    pipeline = [
        {"$match": {"user_id": user_id}},
        {
            "$project": {
                "claims": {
                    "$filter": {
                        "input": "$claims",
                        "as": "claim",
                        "cond": {"$eq": ["$$claim.claim_id", claim_id]},
                    }
                }
            }
        },
    ]
    cursor = claims_collection.aggregate(pipeline)
    result = await cursor.to_list(length=1)

    if not result or not result[0]["claims"]:
        raise HTTPException(status_code=404, detail="Claim not found for user")

    return Response(
        content=dumps(result[0]["claims"][0]), media_type="application/json"
    )


@api_app.get("/pas/{user_id}", operation_id="get_all_pa_requests")
async def get_all_pa_requests(user_id: str):
    """Fetch all PA requests for a given user."""
    doc = await pa_collection.find_one({"user_id": user_id})
    if not doc or "pa_requests" not in doc:
        raise HTTPException(
            status_code=404, detail="No PA requests found for this user"
        )

    return Response(content=dumps(doc["pa_requests"]), media_type="application/json")


@api_app.get("/pas/{user_id}/{pa_id}", operation_id="get_pa_request_by_id")
async def get_pa_request_by_id(user_id: str, pa_id: str):
    """Fetch a specific PA request for a user by pa_id using aggregation."""
    pipeline = [
        {"$match": {"user_id": user_id}},
        {"$unwind": "$pa_requests"},
        {"$match": {"pa_requests.pa_id": pa_id}},
        {"$replaceRoot": {"newRoot": "$pa_requests"}},
    ]

    cursor = pa_collection.aggregate(pipeline)
    result = await cursor.to_list(length=1)

    if not result:
        raise HTTPException(status_code=404, detail="PA request not found for user")

    return Response(content=dumps(result[0]), media_type="application/json")


if __name__ == "__main__":
    import uvicorn

    mcp = FastApiMCP(
        api_app,
        include_operations=[
            "get_all_claims",
            "get_claim_by_id",
            "get_all_pa_requests",
        ],
    )
    mcp.mount()
    # You can customize host, port, log_level, and other uvicorn settings here.
    # Using port 8001 to distinguish from a potential main app on 8000.
    uvicorn.run(api_app, host="0.0.0.0", port=8000)
