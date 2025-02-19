from datetime import timedelta

from telegram import Update, ChatPermissions
from admin import get_user_from_reply, is_possible_to_use
from config import CHAT_ID, ALLOWED_IDS, ADMINS_ID


async def grant(update: Update, context):
    if await is_possible_to_use(update) is False:
        return

    user = await get_user_from_reply(update)
    if user is None:
        return

    await context.bot.promote_chat_member(
        chat_id=CHAT_ID,
        user_id=user.id,
        can_post_messages=True,
        can_manage_chat=True
    )

    if len(update.message.text.split()) < 2:
        await update.message.reply_text(
            'Prosim, napiste v tomto formate /grant userTitul.',
            parse_mode="HTML"
        )
        return

    new_title = " ".join(update.message.text.split()[1:])

    await context.bot.set_chat_administrator_custom_title(
        chat_id=CHAT_ID,
        user_id=user.id,
        custom_title=new_title
    )

    await update.message.reply_text(
        f'Novy titul {user.full_name}: {new_title}',
        parse_mode="HTML"
    )


async def bless(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return

    boosts = await context.bot.get_user_chat_boosts(chat_id=CHAT_ID, user_id=update.message.from_user.id)
    if (not boosts.boosts) is True:
        await update.message.reply_text(
            'Ste taky ledačy, že nemožete používať tento príkaz. Povoleny len pre boosterov!',
            parse_mode="HTML"
        )
        return

    chat_admins = await context.bot.get_chat_administrators(chat_id=CHAT_ID)
    user_is_admin = any(admin.user.id == update.message.from_user.id for admin in chat_admins)
    if not user_is_admin:
        await context.bot.promote_chat_member(
            chat_id=CHAT_ID,
            user_id=update.message.from_user.id,
            can_post_messages=True,
            can_manage_chat=True
        )

    if len(update.message.text.split()) < 2:
        await update.message.reply_text(
            'Prosim, napiste v tomto formate /bless VasTitul.',
            parse_mode="HTML"
        )
        return

    new_title = " ".join(update.message.text.split()[1:])

    await context.bot.set_chat_administrator_custom_title(
        chat_id=CHAT_ID,
        user_id=update.message.from_user.id,
        custom_title=new_title
    )

    await update.message.reply_text(
        f'Tvoj novy titul: {new_title}',
        parse_mode="HTML"
    )


async def meme(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return False
    if update.message.from_user.id in ADMINS_ID:
        await update.message.reply_text(f"Nepovedam ti nič.")
        return

    until_date = update.message.date + timedelta(seconds=180)
    restriction = ChatPermissions(can_send_messages=False)
    await context.bot.restrict_chat_member(chat_id=update.effective_chat.id, user_id=update.message.from_user.id,
                                           permissions=restriction,
                                           until_date=until_date)

    await update.message.reply_text(f"Ledač {update.message.from_user.full_name} zaspal na 180 sekúnd.")
