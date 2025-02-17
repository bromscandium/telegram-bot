from telegram.ext import CommandHandler, ApplicationBuilder, MessageHandler, filters

from commands import *
from admin import *
from interactions import welcome, reaction
from chat import start, start_message
from custom import bless, grant

from config import TOKEN


def main():
    bot = ApplicationBuilder().token(TOKEN).build()

    bot.add_handler(CommandHandler("start", start))

    bot.add_handler(CommandHandler("help", help))

    bot.add_handler(CommandHandler("rules", rules))
    bot.add_handler(CommandHandler("moodle_passwords", moodle_passwords))
    bot.add_handler(CommandHandler("links", links))
    bot.add_handler(CommandHandler("scores", scores))
    bot.add_handler(CommandHandler("map_tuke", map_tuke))
    bot.add_handler(CommandHandler("map_5p", map_5p))
    bot.add_handler(CommandHandler("plan", plan))
    bot.add_handler(CommandHandler("schedule", schedule))
    bot.add_handler(CommandHandler("studijne", studijne))
    bot.add_handler(CommandHandler("invite", invite))

    bot.add_handler(CommandHandler("ban", ban))
    bot.add_handler(CommandHandler("mute", mute))
    bot.add_handler(CommandHandler("unmute", unmute))
    bot.add_handler(CommandHandler("unban", unban))

    bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    bot.add_handler(
        MessageHandler(filters.ALL & (filters.ChatType.GROUP | filters.ChatType.SUPERGROUP) & ~filters.COMMAND,
                       reaction))
    bot.add_handler(MessageHandler(filters.ALL & filters.ChatType.PRIVATE & ~filters.COMMAND, start_message))

    bot.add_handler(CommandHandler("bless", bless))
    bot.add_handler(CommandHandler("grant", grant))
    bot.add_handler(CommandHandler("meme", grant))

    print("Starting Telegram Bot...")
    bot.run_polling(drop_pending_updates=True)


if __name__ == '__main__':
    main()
