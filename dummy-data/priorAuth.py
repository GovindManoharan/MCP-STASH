from fastapi import FastAPI, HTTPException, Response
from motor.motor_asyncio import AsyncIOMotorClient
from bson.json_util import dumps
import os

app = FastAPI()

# MongoDB connection settings
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "call_center_db"
PA_COLLECTION_NAME = "pa_requests"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
pa_collection = db[PA_COLLECTION_NAME]


@app.get("/pas/{user_id}")
async def get_all_pa_requests(user_id: str):
    """Fetch all PA requests for a given user."""
    doc = await pa_collection.find_one({"user_id": user_id})
    if not doc or "pa_requests" not in doc:
        raise HTTPException(
            status_code=404, detail="No PA requests found for this user"
        )

    return Response(content=dumps(doc["pa_requests"]), media_type="application/json")


@app.get("/pas/{user_id}/{pa_id}")
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
