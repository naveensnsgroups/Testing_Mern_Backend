import sys
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

class Database:
    client: AsyncIOMotorClient = None

db = Database()

async def connect_to_mongo():
    if not settings.MONGO_URI:
        print("MONGO_URI is not defined in environment variables.", file=sys.stderr)
        sys.exit(1)
    try:
        db.client = AsyncIOMotorClient(settings.MONGO_URI)
        await db.client.admin.command('ping')
        print(f"MongoDB Atlas Connected successfully")
    except Exception as error:
        print(f"MongoDB Connection Error: {error}", file=sys.stderr)
        sys.exit(1)

async def close_mongo_connection():
    if db.client:
        db.client.close()
        print("MongoDB connection closed.")

def get_db():
    uri = settings.MONGO_URI
    db_name = "personal_details_db"
    if "?" in uri:
        base_part = uri.split("?")[0]
    else:
        base_part = uri
    parts = base_part.split("/")
    if len(parts) >= 4 and parts[3]:
        db_name = parts[3]
    return db.client[db_name]

def get_employee_collection():
    database = get_db()
    return database["HR"]
