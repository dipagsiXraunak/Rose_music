import os
from dotenv import load_dotenv

load_dotenv()

# Required (These MUST be set in environment variables)
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
MONGO_URL = os.getenv("MONGO_URL")

# Optional (These have defaults)
SESSION_STRING = os.getenv("SESSION_STRING", "")
LOGGER_ID = int(os.getenv("LOGGER_ID")) if os.getenv("LOGGER_ID") else 0
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")

# Links (Optional)
SUPPORT_LINK = os.getenv("SUPPORT_LINK", "https://t.me/roseXsupport")
UPDATE_LINK = os.getenv("UPDATE_LINK", "https://t.me/RoseXupdate")
OWNER_LINK = os.getenv("OWNER_LINK", "https://t.me/MalikX_owner")
SOURCE_LINK = os.getenv("SOURCE_LINK", "https://t.me/MalikX_owner")

# Images (Optional)
THUMBNAIL_URL = os.getenv("THUMBNAIL_URL", "https://files.catbox.moe/1")
WELCOME_IMAGE_URL = os.getenv("WELCOME_IMAGE_URL", "https://files.catbox.moe/1")
