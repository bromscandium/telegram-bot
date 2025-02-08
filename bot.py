from telegram.ext import CommandHandler, ApplicationBuilder, MessageHandler, filters
from commands import *
from interactions import (
    welcome, reaction
)
from admin import *
from config import TOKEN


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

    bot.add_handler(CommandHandler("ban", ban))
    bot.add_handler(CommandHandler("mute", mute))
    bot.add_handler(CommandHandler("unmute", unmute))
    bot.add_handler(CommandHandler("unban", unban))

    bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reaction))

    print("Starting Telegram Bot...")
    bot.run_polling(drop_pending_updates=True)


if __name__ == '__main__':
    main()
