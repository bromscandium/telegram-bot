import os
from datetime import datetime

# Variables from .env
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
ADMINS_ID = list(map(int, os.getenv("ADMINS_ID", "").split(",")))
DATABASE = os.getenv("DATABASE")
LINK = os.getenv("LINK")

# Constant variables
REACTIONS = ["5454327849936755071", "5460732483693714384", "5456433487718390163", "5458370788551825969", "5465539720329043304", "5465539720329043304", "5348030016405906262", "5363818603948812235"]
SEMESTER_START = datetime(2025, 2, 10)
