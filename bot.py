from telegram.ext import CommandHandler, ApplicationBuilder, MessageHandler, filters
from commands import *
from config import TOKEN
from interactions import (
    welcome,
)


def main():
    bot = ApplicationBuilder().token(TOKEN).build()

    bot.add_handler(CommandHandler("help", help))
    bot.add_handler(CommandHandler("schedule", schedule))
    bot.add_handler(CommandHandler("rules", rules))
    bot.add_handler(CommandHandler("moodle_passwords", moodle_passwords))
    bot.add_handler(CommandHandler("links", links))
    bot.add_handler(CommandHandler("scores", scores))
    bot.add_handler(CommandHandler("map_tuke", map_tuke))
    bot.add_handler(CommandHandler("map_5p", map_5p))
    bot.add_handler(CommandHandler("studijne", studijne))

    bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))

    print("Starting Telegram Bot...")
    bot.run_polling()


if __name__ == '__main__':
    main()
