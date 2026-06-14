from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

# Global variable for client (will be initialized in init_db)
_db_client = None
_database = None

async def get_db():
    """Get database instance (lazy initialization)"""
    global _db_client, _database
    if _db_client is None:
        if not MONGO_URL or MONGO_URL.startswith("your_"):
            raise ValueError("MONGO_URL is not set correctly")
        _db_client = AsyncIOMotorClient(MONGO_URL)
        _database = _db_client.RoseMusic
        # Test connection
        await _db_client.admin.command('ping')
        print("✅ MongoDB connected successfully")
    return _database

async def init_db():
    """Initialize database collections and indexes"""
    db = await get_db()
    # Create collections if needed
    await db.users.create_index("user_id", unique=True)
    await db.groups.create_index("chat_id", unique=True)
    print("✅ Database indexes created")
