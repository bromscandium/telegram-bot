# Telegram Bot

## Overview

This is a **modular Telegram bot** built in Python, designed to handle various user interactions and commands. It includes an **administrative panel** for managing bot features and is optimized for **local use**. If you wish to run it on a server for persistent storage and processing, you can easily customize the backend.

---

## Features

- **User Command Handling** — Structured and expandable command system.
- **Admin Panel** — Manage users, settings, and features.
- **Modular Architecture** — Organized codebase for easy maintenance and scaling.
- **Configurable via `config.py`** — Centralized configuration management.
- **Database Integration** — Uses PostgreSQL for persistent data storage (for warnings and user data).

---

## File Structure

```
telegram-bot/
├── .gitignore          # List of ignored files
├── admin.py            # Admin-specific functionalities
├── bot.py              # Main entry point of the bot
├── chat.py             # Chat processing functions
├── commands.py         # User command handling
├── config.py           # Bot configuration file
├── interactions.py     # User interaction logic
├── db.py               # Centralized DB connection
├── .env                # Environment variables (not committed)
├── README.md           # Project documentation
├── requirements.txt    # List of Python dependencies
```

---

## Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/bromscandium/telegram-bot
cd telegram-bot
```

### 2️⃣ Install Dependencies

Ensure you have Python 3.x installed. Then install required libraries:

```bash
pip install -r requirements.txt
```

### 3️⃣ Set up Environment Variables

Create a `.env` file in the root of the project directory and add the following variables:

```env
TOKEN=YOUR_BOT_API_TOKEN
CHAT_ID=YOUR_CHAT_ID
ADMIN_CHAT_ID=YOUR_ADMIN_CHAT_ID
ADMINS_ID=YOUR_ADMIN_USER_IDS
DATABASE=YOUR_DATABASE_URL
LINK=YOUR_LINK
```

### 4️⃣ Run the Bot

```bash
python bot.py
```

---

## Dependencies

- **Python 3.x**
- **pip** (Python package manager)
- All required libraries listed in `requirements.txt`

---

## License

This project is open-source. Feel free to use, modify, and distribute it under the terms provided (if applicable).