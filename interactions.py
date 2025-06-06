import random
from datetime import timedelta

from admin import is_possible
from commands import personal_limit_usage
from config import REACTIONS, CHAT_ID, ADMINS_ID
from telegram import Update, ChatPermissions, ReactionTypeCustomEmoji

message_counter = 0
next_reaction = random.randint(1, 10)


# Interactions with users

async def welcome(update: Update, context):
    if update.message.new_chat_members:
        for user in update.message.new_chat_members:
            await update.message.reply_text(
                f"Vítam ťa, <b>ledáč {user.full_name}</b>.\n\n"
                "Nepýtam sa, prečo si tu, ale ak chceš prežiť dlhšie ako pár dní, prestaň lajdáčiť "
                "(ледарствувати? байдикувати?) a okamžite si prečítaj <b>ASAP</b>.\n\n"
                "Áno, viem, je to veľa textu – no ak si doteraz prežil KM, mal by si byť schopný prečítať aspoň pár viet.\n\n"
                "📌 Čo tam nájdeš?\n\n"
                "Pravidlá – ak ich porušíš, nebude ma zaujímať, že si ich \"nečítal\".\n\n"
                "Navigáciu – aby ste vedeli, kde klásť svoje (dúfam, že inteligentné) otázky\n\n"
                "Dôležité termíny, materiály – aby si nebol ako tí, čo odovzdávajú CopyMaster po deadline "
                "a nespočetne krát strácajú môj čas svojou neschopnosťou.\n\n"
                "❗️ Zapni si notifikácie na <b>ASAP</b>. Ak ich vypneš a premeškáš niečo dôležité, "
                "urobím presne nič, aby som ti pomohol.\n\n"
                "Uvidíme, či z teba niečo bude, alebo skončíš v tradičnom zozname.",
                parse_mode="HTML"
            )


async def reaction(update: Update, context):
    global message_counter, next_reaction
    if update.message:
        message_counter += 1
        if message_counter >= next_reaction:
            emoji_id = random.choice(REACTIONS)
            await context.bot.set_message_reaction(
                chat_id=update.message.chat_id,
                message_id=update.message.message_id,
                reaction=[ReactionTypeCustomEmoji(custom_emoji_id=emoji_id)],
                is_big=False
            )
            message_counter = 0

            next_reaction = random.randint(1, 10)

@personal_limit_usage(12000)
async def bless(update: Update, context):
    if await is_possible(update, 'can_promote_members'):
        return

    boosts = await context.bot.get_user_chat_boosts(chat_id=CHAT_ID, user_id=update.message.from_user.id)
    if (not boosts.boosts) is True:
        await update.message.reply_text('Povoleny len pre boosterov!')
        return

    if len(update.message.text.split()) < 2:
        await update.message.reply_text('Prosim, napiste v tomto formate: /bless VasTitul.')
        return
    new_title = " ".join(update.message.text.split()[1:])

    chat_admins = await context.bot.get_chat_administrators(chat_id=CHAT_ID)
    user_is_admin = any(admin.user.id == update.message.from_user.id for admin in chat_admins)
    if not user_is_admin:
        await context.bot.promote_chat_member(
            chat_id=CHAT_ID,
            user_id=update.message.from_user.id,
            can_post_messages=True,
            can_manage_chat=True
        )

    await context.bot.set_chat_administrator_custom_title(
        chat_id=CHAT_ID,
        user_id=update.message.from_user.id,
        custom_title=new_title
    )
    await update.message.reply_text(f'Tvoj novy titul: {new_title}')


async def meme(update: Update, context):
    if update.message.from_user.id in ADMINS_ID:
        return

    await context.bot.restrict_chat_member(chat_id=update.effective_chat.id, user_id=update.message.from_user.id,
                                           permissions=ChatPermissions.no_permissions(),
                                           until_date=update.message.date + timedelta(seconds=180))

    await update.message.reply_text(f"Ledač {update.message.from_user.full_name} zaspal na 180 sekúnd.")
