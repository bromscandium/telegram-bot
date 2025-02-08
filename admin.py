from datetime import timedelta

from telegram import Update, ChatPermissions

from config import ALLOWED_IDS


async def is_admin(update: Update) -> bool:
    chat_member = await update.effective_chat.get_member(update.effective_user.id)

    if chat_member.status not in ['administrator', 'creator']:
        return False

    admins = await update.effective_chat.get_administrators()

    for admin in admins:
        if admin.user.id == update.effective_user.id:
            return admin.can_restrict_members

    return False


async def get_user_from_message_or_username(update: Update, context):
    if update.message.reply_to_message:
        return update.message.reply_to_message.from_user, 0
    elif len(context.args) > 0 and context.args[0].startswith('@'):
        username = context.args[0][1:]
        members = await context.bot.get_chat_administrators(update.effective_chat.id)
        user = next((member.user for member in members if member.user.username == username), None)
        if user is None:
            await update.message.reply_text(f"Ледацюгу @{username} не знайдено.")
            return None, None
        return user, 1
    return None, None


async def mute(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return
    if not await is_admin(update):
        await update.message.reply_text("Такі ледацюги як ти не можуть використовувати цю команду.")
        return

    user, index = await get_user_from_message_or_username(update, context)
    if user is None:
        await update.message.reply_text(
            "Використовуйте: /mute @username [час] або відповідайте на повідомлення.")
        return
    duration = int(context.args[index]) if len(context.args) > index else 0
    if 59 > duration > 1:
        duration = 60

    until_date = None if duration == 0 else update.message.date + timedelta(seconds=duration)
    permissions = ChatPermissions(can_send_messages=False)
    await context.bot.restrict_chat_member(chat_id=update.effective_chat.id,
                                           user_id=user.id,
                                           permissions=permissions,
                                           until_date=until_date)

    if duration == 0:
        await update.message.reply_text(f"Ледацюгу {user.full_name} зам'ючено.")
    else:
        await update.message.reply_text(f"Ледацюгу {user.full_name} зам'ючено на {duration} секунд.")


async def unmute(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return
    if not await is_admin(update):
        await update.message.reply_text("Такі ледацюги як ти не можуть використовувати цю команду.")
        return

    user, _ = await get_user_from_message_or_username(update, context)
    if user is None:
        await update.message.reply_text(
            "Використовуйте: /unmute @username або відповідайте на повідомлення.")
        return

    permissions = ChatPermissions(can_send_messages=True)
    await context.bot.restrict_chat_member(chat_id=update.effective_chat.id,
                                           user_id=user.id,
                                           permissions=permissions)
    await update.message.reply_text(f"Ледацюгу {user.full_name} розм'ючено.")


async def ban(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return
    if not await is_admin(update):
        await update.message.reply_text("Такі ледацюги як ти не можуть використовувати цю команду.")
        return

    user, _ = await get_user_from_message_or_username(update, context)
    if user is None:
        await update.message.reply_text(
            "Використовуйте: /ban @username або відповідайте на повідомлення.")
        return

    await context.bot.ban_chat_member(chat_id=update.effective_chat.id, user_id=user.id)
    await update.message.reply_text(f"Ледацюгу {user.full_name} заблоковано.")


async def unban(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return
    if not await is_admin(update):
        await update.message.reply_text("Такі ледацюги як ти не можуть використовувати цю команду.")
        return

    user, _ = await get_user_from_message_or_username(update, context)
    if user is None:
        await update.message.reply_text(
            "Використовуйте: /unban @username або відповідайте на повідомлення.")
        return

    await context.bot.unban_chat_member(chat_id=update.effective_chat.id, user_id=user.id)
    await update.message.reply_text(f"Ледацюгу {user.full_name} розблоковано.")
