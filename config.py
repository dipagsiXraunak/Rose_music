import os
from dotenv import load_dotenv
load_dotenv()

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OWNER_ID = int(os.getenv("OWNER_ID", 0))
SESSION_STRING = os.getenv("SESSION_STRING", "")
LOGGER_ID = int(os.getenv("LOGGER_ID", 0))

# Your links — default to yours if env not set
SUPPORT_LINK = os.getenv("SUPPORT_LINK", "https://t.me/roseXsupport")
UPDATE_LINK = os.getenv("UPDATE_LINK", "https://t.me/RoseXupdate")
OWNER_LINK  = os.getenv("OWNER_LINK", "https://t.me/MalikX_owner")
SOURCE_LINK = os.getenv("SOURCE_LINK", "https://t.me/MalikX_owner")

# Your custom images — default to yours
THUMBNAIL_URL = os.getenv("THUMBNAIL_URL", "https://files.catbox.moe/1rj2q2.jpg")
WELCOME_IMAGE_URL = os.getenv("WELCOME_IMAGE_URL", "https://files.catbox.moe/9q73nt.jpg")

# YouTube API (stored, not used directly by yt-dlp)
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "AIzaSyBza3ew7sdakHkF3irNQwRotoXi_6q84ug")
