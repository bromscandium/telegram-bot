import re
from datetime import timedelta
from telegram import Update, ChatPermissions
from config import ALLOWED_IDS, ADMINS_ID

CONFIG_FILE = "config.py"


async def is_admin(update: Update) -> bool:
    chat_member = await update.effective_chat.get_member(update.effective_user.id)

    if chat_member.status not in ['administrator', 'creator']:
        return False

    admins = await update.effective_chat.get_administrators()

    for admin in admins:
        if admin.user.id == update.effective_user.id:
            return admin.can_restrict_members

    return False


async def get_user_from_reply(update: Update) -> 'User':
    user = update.message.reply_to_message.from_user
    if user is None:
        await update.message.reply_text(f'Ledač neexistuje.', parse_mode="HTML")
        return None
    return user


async def is_possible_to_use(update: Update) -> bool:
    if update.message.chat.id not in ALLOWED_IDS:
        return False

    if not await is_admin(update):
        await update.message.reply_text("Ledači ako ty nemôžu používať tento príkaz.")
        return False


async def mute(update: Update, context):
    if await is_possible_to_use(update) is False:
        return

    user = await get_user_from_reply(update)
    if user is None:
        return

    if user.id in ADMINS_ID:
        await update.message.reply_text(f"{user.full_name} je administrátor, nemôže byť umlčaný.")
        return

    duration = int(context.args[0]) if len(context.args) > 0 else 0
    if 59 > duration > 1:
        duration = 60

    until_date = None if duration == 0 else update.message.date + timedelta(seconds=duration)
    restriction = ChatPermissions(can_send_messages=False)
    await context.bot.restrict_chat_member(chat_id=update.effective_chat.id, user_id=user.id, permissions=restriction,
                                           until_date=until_date)

    if duration == 0:
        await update.message.reply_text(f"Ledač {user.full_name} zaspal.")
    else:
        await update.message.reply_text(f"Ledač {user.full_name} bude spať {duration} sekúnd.")


async def unmute(update: Update, context):
    if await is_possible_to_use(update) is False:
        return

    user = await get_user_from_reply(update)
    if user is None:
        return

    permissions = ChatPermissions(can_send_messages=True, can_send_videos=True, can_send_photos=True,
                                  can_send_audios=True, can_send_documents=True, can_send_polls=True,
                                  can_send_voice_notes=True, can_send_video_notes=True, can_add_web_page_previews=True,
                                  can_send_other_messages=True)

    await context.bot.restrict_chat_member(chat_id=update.effective_chat.id, user_id=user.id, permissions=permissions)
    await update.message.reply_text(f"Ledač {user.full_name} sa zobudil.")


async def ban(update: Update, context):
    if await is_possible_to_use(update) is False:
        return

    user = await get_user_from_reply(update)
    if user is None:
        return

    if user.id in ADMINS_ID:
        await update.message.reply_text(f"{user.full_name} je administrátor, nemôže byť umlčaný.")
        return

    await context.bot.ban_chat_member(chat_id=update.effective_chat.id, user_id=user.id)
    await update.message.reply_text(f"Ledač {user.full_name} zaspal navždy.")


async def unban(update: Update, context):
    if await is_possible_to_use(update) is False:
        return

    user = await get_user_from_reply(update)
    if user is None:
        return

    await context.bot.unban_chat_member(chat_id=update.effective_chat.id, user_id=user.id)
    await update.message.reply_text(f"Ledač {user.full_name} sa môže zobudiť.")


async def change(update: Update, context):
    if await is_possible_to_use(update) is False:
        return

    new_id = update.message.reply_to_message.message_id

    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        content = file.read()

    updated_content = re.sub(r"^TODOLIST_ID\s*=\s*\d+", f"TODOLIST_ID = {new_id}", content, flags=re.MULTILINE)

    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        file.write(updated_content)
