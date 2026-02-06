import os
from typing import  Any
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv



load_dotenv()

# Support multiple env names: prefer MONGODB_URL, fall back to MONGO_URL
MONGODB_URL = os.getenv("MONGODB_URL") or os.getenv("MONGO_URL") or "mongodb://localhost:27017"
# Database name
DATABASE_NAME = os.getenv("DATABASE_NAME", "hrms_lite")

# Global client + database instances
client: Any = None
db: Any = None


async def connect_db() -> None:
    """Connect to MongoDB and create needed indexes."""
    global client, db
    if client is not None:
        return

    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]

    # Create indexes for unique fields
    await db["employees"].create_index("employee_id", unique=True)
    await db["employees"].create_index("email", unique=True)
    await db["attendance"].create_index([("employee_id", 1), ("date", 1)], unique=True)

    print(f"✓ Connected to MongoDB database: {DATABASE_NAME}")


async def close_db() -> None:
    """Close MongoDB connection if open."""
    global client, db
    if client is not None:
        client.close()
        client = None
        db = None
        print("✓ Disconnected from MongoDB")


def get_db() -> "Any":
    """Get database instance (raises if not connected)."""
    if db is None:
        raise RuntimeError("Database not connected. Call connect_db() first.")
    return db
