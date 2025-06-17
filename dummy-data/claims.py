from fastapi import FastAPI, HTTPException, Response
from motor.motor_asyncio import AsyncIOMotorClient
from bson.json_util import dumps
import os

app = FastAPI()

# MongoDB connection settings
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "call_center_db"
COLLECTION_NAME = "claims"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
claims_collection = db[COLLECTION_NAME]


@app.get("/claims/{user_id}")
async def get_all_claims(user_id: str):
    doc = await claims_collection.find_one({"user_id": user_id})
    if not doc:
        raise HTTPException(status_code=404, detail="No claims found for this user")
    return Response(content=dumps(doc), media_type="application/json")


@app.get("/claims/{user_id}/{claim_id}")
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
