from telegram.ext import ApplicationBuilder
from handlers import start
from config import TOKEN

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Starting Telegram Bot...")
    app.run_polling()


if __name__ == "__main__":
    main()
