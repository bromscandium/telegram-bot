from telegram import Update

from config import ADMIN_CHAT_ID

user_state = {}


async def start(update: Update, context):
    user_id = update.message.from_user.id

    if update.message.chat.type == "private":
        user_state[user_id] = 'waiting_for_message'
        await update.message.reply_text("Привіт! Напишіть ваше повідомлення, і я відправлю його в групу.")


async def handle_message(update: Update, context):
    chat_type = update.message.chat.type
    if chat_type != 'private':
        return

    user_id = update.message.from_user.id
    username = update.message.from_user.username
    fullname = update.message.from_user.full_name

    if user_id in user_state and user_state[user_id] == 'waiting_for_message':
        text_to_send = ""
        if update.message.text is not None:
            text_to_send = update.message.text if update.message.text else ""
        elif update.message.caption is not None:
            text_to_send = update.message.caption if update.message.caption else ""
        text_to_send += f"\n\n#пишутьгенчі\nid{user_id}\n@{username}\n{fullname}"
        if update.message.text:
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=text_to_send)

        if update.message.photo:
            await context.bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=update.message.photo[-1].file_id,
                                         caption=text_to_send)
        elif update.message.video:
            await context.bot.send_video(chat_id=ADMIN_CHAT_ID, video=update.message.video.file_id,
                                         caption=text_to_send)

        await update.message.reply_text("Ваше повідомлення було надіслано в групу.")

        user_state[user_id] = 'message_sent'
