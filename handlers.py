from telegram import Update
from telegram.ext import CommandHandler

async def start(update: Update, context):
    await update.message.reply_text("Ти даун?")