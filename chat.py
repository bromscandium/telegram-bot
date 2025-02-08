from telegram import Update

from config import ADMIN_CHAT_ID

user_state = {}


async def start(update: Update, context):
    user_id = update.message.from_user.id

    if update.message.chat.type == "private":
        user_state[user_id] = 'waiting_for_message'
        await update.message.reply_text("Привіт! Напишіть ваше повідомлення, і я відправлю його в групу.")


async def handle_message(update: Update, context):
    user_id = update.message.from_user.id

    if user_id in user_state and user_state[user_id] == 'waiting_for_message':
        if update.message.text:
            text_to_send = update.message.text

        text_to_send += "\n#пишутьгенчі"

        if update.message.text:
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=text_to_send)
        elif update.message.photo:
            await context.bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=update.message.photo[-1].file_id,
                                         caption=text_to_send)
        elif update.message.video:
            await context.bot.send_video(chat_id=ADMIN_CHAT_ID, video=update.message.video.file_id,
                                         caption=text_to_send)

        await update.message.reply_text("Ваше повідомлення було надіслано в групу.")

        user_state[user_id] = 'message_sent'
