from telegram import Update


async def forward_news(update: Update, context):
    if update.effective_chat.id == CHANNEL_ID:
        print("test")
