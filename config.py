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
REACTIONS = ["5454327849936755071", "5458820832404970974", "5460677478047554090","5456433487718390163","5197508012729703159","5321450521100295815","5363818603948812235","5465185664699997841"]
SEMESTER_START = datetime(2025, 2, 10)
