import atexit

from telegram import MessageEntity

from database import conn, cursor
from telegram.ext import CommandHandler, ApplicationBuilder, MessageHandler, filters
from admin import *
from chat import *
from commands import *
from interactions import *
from config import TOKEN


# Launching bot by importing commands
def main():
    bot = ApplicationBuilder().token(TOKEN).build()

    commands = {
        "mute": mute,
        "unmute": unmute,
        "ban": ban,
        "unban": unban,
        "listwarn": listwarn,
        "warn": warn,
        "unwarn": unwarn,
        "resetwarn": resetwarn,
        # "grant": grant,
        # "ungrant": ungrant,
        "start": start,
        # "help": help,
        "rules": rules,
        "moodle": moodle,
        "links": links,
        "scores": scores,
        "plan": plan,
        "maptuke": maptuke,
        "map5p": map5p,
        "studijne": studijne,
        "schedule": schedule,
        "invite": invite,
        "week": week,
        # "bless": bless,
        "meme": meme,
        "predict": predict,
        "weather": weather,
        "chance": chance
        # "setnick": setnick
    }

    for command, handler in commands.items():
        bot.add_handler(CommandHandler(command, handler))

    bot.add_handler(MessageHandler(filters.ChatType.PRIVATE & ~filters.COMMAND, start_message))
    bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    bot.add_handler(MessageHandler(filters.ChatType.GROUP | filters.ChatType.SUPERGROUP & ~filters.COMMAND, reaction))

    print("Starting Telegram Bot...")
    bot.run_polling(drop_pending_updates=True)


def close_db():
    print("Closing database connection...")
    cursor.close()
    conn.close()


if __name__ == '__main__':
    main()

atexit.register(close_db)
