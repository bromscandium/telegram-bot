from telegram import Update, ChatPermissions, Chat
from telegram.ext import CallbackContext
from datetime import timedelta, datetime

from commands import personal_limit_usage
from database import *

from config import ADMINS_ID, GRANT_ADMINS_ID, CHAT_ID


# Checking function

async def is_possible(update, required_permission: str, use_grant_admins=False) -> bool:
    allowed_ids = GRANT_ADMINS_ID if use_grant_admins else ADMINS_ID

    if update.message.from_user.id not in allowed_ids:
        await update.message.reply_text("Ledači ako ty nemôžu používať tento príkaz.")
        return False

    user = update.message.reply_to_message.from_user
    if user is None:
        await update.message.reply_text(f'Ledač neexistuje.')
        return False

    if user.id in ADMINS_ID:  # головних адміністраторів все одно не можна чіпати
        await update.message.reply_text(f"{user.full_name} je hlavny administrátor.")
        return False

    chat_administrators = await update.effective_chat.get_administrators()
    for admin in chat_administrators:
        if admin.user.id == update.message.from_user.id:
            if getattr(admin, required_permission, False):
                return True
            else:
                await update.message.reply_text(f"{admin.user.full_name} nema tejto moznosti.")
                return False
    return True


# Basic admin functions

async def mute(update: Update, context):
    if not await is_possible(update, 'can_restrict_members'):
        return

    user = update.message.reply_to_message.from_user
    duration = int(context.args[0]) if len(context.args) > 0 else 0
    if duration < 59:
        duration = 60
    until_date = None if duration == 0 else update.message.date + timedelta(seconds=duration)

    await context.bot.restrict_chat_member(chat_id=update.effective_chat.id, user_id=user.id,
                                           permissions=ChatPermissions.no_permissions(),
                                           until_date=until_date)
    await update.message.reply_text(f"Ledač {user.full_name} zaspal.")


async def unmute(update: Update, context):
    if not await is_possible(update, 'can_restrict_members'):
        return

    user = update.message.reply_to_message.from_user

    await context.bot.restrict_chat_member(chat_id=update.effective_chat.id, user_id=user.id,
                                           permissions=ChatPermissions.all_permissions())
    await update.message.reply_text(f"Ledač {user.full_name} sa zobudil.")


async def ban(update: Update, context):
    if not await is_possible(update, 'can_restrict_members'):
        return

    user = update.message.reply_to_message.from_user

    await context.bot.ban_chat_member(chat_id=update.effective_chat.id, user_id=user.id)
    await update.message.reply_text(f"Ledač {user.full_name} zaspal navždy.")


async def unban(update: Update, context):
    if not await is_possible(update, 'can_restrict_members'):
        return

    user = update.message.reply_to_message.from_user

    await context.bot.unban_chat_member(chat_id=update.effective_chat.id, user_id=user.id)
    await update.message.reply_text(f"Ledač {user.full_name} sa môže zobudiť.")


async def grant(update: Update, context, use_grant_admins=True):
    if not await is_possible(update, 'can_promote_members'):
        return

    user = update.message.reply_to_message.from_user

    await context.bot.promote_chat_member(
        chat_id=CHAT_ID,
        user_id=user.id,
        can_post_messages=True,
        can_manage_chat=True
    )

    if len(update.message.text.split()) < 2:
        await update.message.reply_text('Prosim, napiste v tomto formate: /grant userTitul.')
        return

    new_title = " ".join(update.message.text.split()[1:])

    await context.bot.set_chat_administrator_custom_title(
        chat_id=CHAT_ID,
        user_id=user.id,
        custom_title=new_title
    )

    await update.message.reply_text(f'Novy titul {user.full_name}: {new_title}')

@personal_limit_usage(12000)

async def ungrant(update: Update, context, use_grant_admins=True):
    if not await is_possible(update, 'can_promote_members'):
        return

    user = update.message.reply_to_message.from_user

    await context.bot.promote_chat_member(
        chat_id=CHAT_ID,
        user_id=user.id,
        can_change_info=False,
        can_post_messages=False,
        can_edit_messages=False,
        can_delete_messages=False,
        can_invite_users=False,
        can_restrict_members=False,
        can_pin_messages=False,
        can_promote_members=False,
        can_manage_chat=False,
        can_manage_video_chats=False,
        can_manage_topics=False,
        is_anonymous=False
    )

    await update.message.reply_text(f"{user.full_name} už nema titula.")


# Warning admin functions

async def listwarn(update: Update, context):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
    else:
        user = update.message.from_user


    warnings_count = get_warning_count(user.id)
    reasons = get_warning_reasons(user.id)

    if reasons == "—":
        await update.message.reply_text("Tento ledač nemá žiadne varovania.")
    else:
        await update.message.reply_text(f"{user.full_name} má {warnings_count} varovania:\n\n{reasons}")


async def warn(update: Update, context: CallbackContext):
    if not await is_possible(update, 'can_restrict_members'):
        return

    user = update.message.reply_to_message.from_user

    reason = ' '.join(context.args) if context.args else 'Bez dôvodu'

    add_warning(user.id, reason)

    warnings_count = get_warning_count(user.id)

    if warnings_count >= 3:
        until_date = update.message.date + timedelta(days=2)
        await context.bot.restrict_chat_member(chat_id=update.effective_chat.id, user_id=user.id,
                                               permissions=ChatPermissions.no_permissions(), until_date=until_date)
        reset_warnings(user.id)

        await update.message.reply_text(
            f"{user.full_name} dostal {warnings_count} varovaní a bude spat 2 dni."
        )
    else:
        await update.message.reply_text(
            f"{user.full_name} dostal varovanie. Teraz má {warnings_count}."
        )


async def unwarn(update: Update, context):
    if not await is_possible(update, 'can_restrict_members'):
        return

    user = update.message.reply_to_message.from_user

    reset_warnings(user.id)

    await update.message.reply_text(f"Všetky varovania boli vymazané z ledača {user.full_name}.")


async def resetwarn(update: Update, context):
    if not getattr(await update.effective_chat.get_member(update.effective_user.id), 'can_restrict_members', False):
        await update.message.reply_text(f"{update.effective_user.full_name} nema tejto moznosti.")
        return False

    cursor.execute("UPDATE warnings SET warnings = 0")
    conn.commit()

    await context.bot.send_message(chat_id=CHAT_ID, text="Všetky varovania boli automaticky resetované!")
