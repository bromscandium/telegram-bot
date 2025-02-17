from telegram import Update

from admin import get_user_from_reply, is_possible_to_use
from config import CHAT_ID, ALLOWED_IDS


async def grant(update: Update, context):
    await is_possible_to_use(update)
    user = await get_user_from_reply(update)
    if user is None:
        return

    await context.bot.promote_chat_member(
        chat_id=CHAT_ID,
        user_id=user.id,
        can_post_messages=True,
        can_manage_chat=True,
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
    if boosts == 0:
        await update.message.reply_text(
            'Ste taky ledačy, že nemožete používať tento príkaz. Povoleny len pre boosterov!',
            parse_mode="HTML"
        )
        return

    chat_admins = await context.bot.get_chat_administrators(chat_id=CHAT_ID)
    user_is_admin = any(admin.user.id == update.message.from_user.id for admin in chat_admins)
    if not user_is_admin:
        result = await context.bot.promote_chat_member(
            chat_id=CHAT_ID,
            user_id=update.message.from_user.id,
            can_change_info=False,
            can_post_messages=True,
            can_edit_messages=False,
            can_delete_messages=False,
            can_invite_users=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_promote_members=False,
            is_anonymous=False,
            can_manage_chat=True,
            can_manage_video_chats=False,
            can_manage_topics=False,
            can_post_stories=False,
            can_edit_stories=False,
            can_delete_stories=False
        )
        print(result)

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
