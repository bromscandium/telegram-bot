from telegram import Update
from config import CHAT_ID, ALLOWED_IDS


async def help(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return
    if update.message:
        await update.message.reply_text(
            '''Čo zase chceš?

Ak už si sa rozhodol otravovať bota, aspoň si vyber správny príkaz:

📅 /schedule – Rozvrh na rok, aj tak si ho nikto poriadne nepozrie.
📜 /rules – Pravidlá, ktoré si aj tak niektorí myslia, že pre nich neplatia
🔐 /moodle_passwords – Heslá k Moodle, pre prípad, že si ich zase zabudol.
🔗 /links – Odkazy na prednášky a cvičenia, ktoré budeš ignorovať až do skúškového.
📊 /scores – Systém hodnotenia, kde sa presvedčíš, že si to opäť pokašľal.
🗺 /map_tuke – Mapa TUKE, lebo po troch rokoch stále netrafíš do správnej miestnosti.
🏛 /map_5p – Mapa 5. poschodia hlavnej budovy, aby si sa tam nestratil ako naposledy.
📩 /studijne – Informácie o študijnom oddelení, kde aj tak neodpovedajú, keď ich potrebuješ.

Ak ešte stále máš otázky, možno je problém inde.''',
            parse_mode="HTML"
        )


async def rules(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return
    if update.message:
        await update.message.reply_text(
            '<a href="https://t.me/c/2307996875/4/52">čítali ste kanál ASAP?</a>',
            parse_mode="HTML"
        )
        await context.bot.copy_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=52
        )


async def moodle_passwords(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return
    if update.message:
        await update.message.reply_text(
            '<a href="https://t.me/c/2307996875/4/56">čítali ste kanál ASAP?</a>',
            parse_mode="HTML"
        )
        await context.bot.copy_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=56
        )


async def links(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return
    if update.message:
        await update.message.reply_text(
            '<a href="https://t.me/c/2307996875/4/57">čítali ste kanál ASAP?</a>',
            parse_mode="HTML"
        )
        await context.bot.copy_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=57
        )


async def scores(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return
    if update.message:
        await update.message.reply_text(
            '<a href="https://t.me/c/2307996875/4/63">čítali ste kanál ASAP?</a>',
            parse_mode="HTML"
        )
        await context.bot.copy_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=63
        )


async def schedule(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return
    if update.message:
        await update.message.reply_text(
            '<a href="https://t.me/c/2307996875/4/67">čítali ste kanál ASAP?</a>',
            parse_mode="HTML"
        )
        await context.bot.copy_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=67
        )


async def map_tuke(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return
    if update.message:
        await update.message.reply_text(
            '<a href="https://t.me/c/2307996875/4/68">čítali ste kanál ASAP?</a>',
            parse_mode="HTML"
        )
        await context.bot.copy_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=68
        )


async def map_5p(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return
    if update.message:
        await update.message.reply_text(
            '<a href="https://t.me/c/2307996875/4/69">čítali ste kanál ASAP?</a>?',
            parse_mode="HTML"
        )
        await context.bot.copy_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=69
        )


async def studijne(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return
    if update.message:
        await update.message.reply_text(
            '<a href="https://t.me/c/2307996875/4/72">čítali ste kanál ASAP?</a>?',
            parse_mode="HTML"
        )
        await context.bot.copy_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=72
        )


async def mute(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return


async def unmute(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return


async def ban(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return


async def unban(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return
