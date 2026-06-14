from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

# Initialize MongoDB client
db_client = AsyncIOMotorClient(MONGO_URL)
database = db_client.RoseMusic

# Collections
users = database.users
groups = database.groups

async def init_db():
    """Initialize database collections and indexes"""
    try:
        # Create indexes for better performance
        await users.create_index("user_id", unique=True)
        await groups.create_index("chat_id", unique=True)
        print("✅ Database connected successfully!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
