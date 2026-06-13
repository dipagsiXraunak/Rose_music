import os
from dotenv import load_dotenv
load_dotenv()

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OWNER_ID = int(os.getenv("OWNER_ID", 0))
SESSION_STRING = os.getenv("SESSION_STRING", "")
LOGGER_ID = int(os.getenv("LOGGER_ID", 0))

SUPPORT_LINK = os.getenv("SUPPORT_LINK", "https://t.me/your_support")
UPDATE_LINK = os.getenv("UPDATE_LINK", "https://t.me/your_update_channel")
OWNER_LINK  = os.getenv("OWNER_LINK", "https://t.me/your_username")
SOURCE_LINK = os.getenv("SOURCE_LINK", "https://github.com/your-username/ROSE-Music-Bot")

THUMBNAIL_URL = os.getenv("THUMBNAIL_URL", "")
WELCOME_IMAGE_URL = os.getenv("WELCOME_IMAGE_URL", "")
