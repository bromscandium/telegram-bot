from telegram import Update

from config import ADMIN_CHAT_ID

user_state = {}


async def start(update: Update, context):
    if update.message.chat.type == 'private':
        user_id = update.message.from_user.id
        user_state[user_id] = 'waiting_for_message'
        await update.message.reply_text("Напишіть ваше повідомлення, і я відправлю його в адміністраторам")


async def start_message(update: Update, context):
    if update.message.chat.type == 'private' and user_state.get(update.message.from_user.id) == 'waiting_for_message':
        await context.bot.forward_message(chat_id=ADMIN_CHAT_ID, from_chat_id=update.message.chat.id,
                                          message_id=update.message.message_id)
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID,
                                       text=f"\n\n#надіслали_в_бота\n<blockquote>id{update.message.from_user.id}\n@{update.message.from_user.username}\n{update.message.from_user.full_name}</blockquote>",
                                       parse_mode="HTML")
        await update.message.reply_text("Ваше повідомлення було надіслано в групу.")

        user_state[update.message.from_user.id] = 'message_sent'
