import os
from datetime import datetime

# Variables from .env
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
ADMINS_ID = list(map(int, os.getenv("ADMINS_ID", "").split(",")))
DATABASE = os.getenv("DATABASE")
LINK = os.getenv("LINK")
BLACKLIST = os.getenv("BLACKLIST")

# Constant variables
REACTIONS = ["🔥", "👍", "😢", "😁", "👎", "🤯", "😎", "🥰"]
SEMESTER_START = datetime(2025, 2, 10)
