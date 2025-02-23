from telegram import Update
from datetime import datetime, timedelta
from config import CHAT_ID, ALLOWED_IDS
from interactions import limit_usage

SEMESTER_START = datetime(2025, 2, 10)


@limit_usage
async def help(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return
    if update.message:
        await update.message.reply_text(
            '''Čo zase chceš?

Ak už si sa rozhodol otravovať bota, aspoň si vyber správny príkaz:

📅 /plan – Rozvrh na rok, aj tak si ho nikto poriadne nepozrie.
🗓️ /schedule – Rozvrh na semester, ktorý si aj tak otvoríš až týždeň pred skúškami.
📜 /rules – Pravidlá, ktoré si aj tak niektorí myslia, že pre nich neplatia
🔐 /moodle_passwords – Heslá k Moodle, pre prípad, že si ich zase zabudol.
🔗 /links – Odkazy na prednášky a cvičenia, ktoré budeš ignorovať až do skúškového.
📊 /scores – Systém hodnotenia, kde sa presvedčíš, že si to opäť pokašľal.
🗺 /map_tuke – Mapa TUKE, lebo po troch rokoch stále netrafíš do správnej miestnosti.
🏛 /map_5p – Mapa 5. poschodia hlavnej budovy, aby si sa tam nestratil ako naposledy.
📩 /studijne – Informácie o študijnom oddelení, kde aj tak neodpovedajú, keď ich potrebuješ.
🔗 /invite – Neverím, že máš priateľov, ale môžeš ich pozvať.
📃 /todolist – Zoznam úloh, ktoré si aj tak nesplníš načas
⭐ /bless – Výhody boosterov, lebo aj tak si si boost kúpil len omylom.
👀 /week – Počet týždňov, čo si premárnil, a koľko ti ostáva na zúfalstvo.

Ak ešte stále máš otázky, možno je problém inde.''',
            parse_mode="HTML"
        )


@limit_usage
async def rules(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return
    if update.message:
        await update.message.reply_text(
            'čítali ste kanál <a href="https://t.me/c/2307996875/4/52">ASAP</a>?',
            parse_mode="HTML"
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Je tam príliš veľa textu, môžete si na tlačidlo kliknúť aj samostatne!",
            message_thread_id=update.message.message_thread_id
        )


@limit_usage
async def moodle_passwords(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return
    if update.message:
        await update.message.reply_text(
            'čítali ste kanál <a href="https://t.me/c/2307996875/4/56">ASAP</a>?',
            parse_mode="HTML"
        )
        await context.bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=56,
            message_thread_id=update.message.message_thread_id,
        )


@limit_usage
async def links(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return
    if update.message:
        await update.message.reply_text(
            'čítali ste kanál <a href="https://t.me/c/2307996875/4/57">ASAP</a>?',
            parse_mode="HTML"
        )
        await context.bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=57,
            message_thread_id=update.message.message_thread_id,
        )


@limit_usage
async def scores(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return
    if update.message:
        await update.message.reply_text(
            'čítali ste kanál <a href="https://t.me/c/2307996875/4/63">ASAP</a>?',
            parse_mode="HTML"
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Je tam príliš veľa textu, môžete si na tlačidlo kliknúť aj samostatne!",
            message_thread_id=update.message.message_thread_id
        )


@limit_usage
async def plan(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return
    if update.message:
        await update.message.reply_text(
            'čítali ste kanál <a href="https://t.me/c/2307996875/4/67">ASAP</a>?',
            parse_mode="HTML"
        )
        await context.bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=67,
            message_thread_id=update.message.message_thread_id
        )


@limit_usage
async def map_tuke(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return
    if update.message:
        await update.message.reply_text(
            'čítali ste kanál <a href="https://t.me/c/2307996875/4/68">ASAP</a>?',
            parse_mode="HTML"
        )
        await context.bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=68,
            message_thread_id=update.message.message_thread_id
        )


@limit_usage
async def map_5p(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return
    if update.message:
        await update.message.reply_text(
            'čítali ste kanál <a href="https://t.me/c/2307996875/4/69">ASAP</a>?',
            parse_mode="HTML"
        )
        await context.bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=69,
            message_thread_id=update.message.message_thread_id
        )


@limit_usage
async def studijne(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return
    if update.message:
        await update.message.reply_text(
            'čítali ste kanál <a href="https://t.me/c/2307996875/4/72">ASAP</a>?',
            parse_mode="HTML"
        )
        await context.bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=72,
            message_thread_id=update.message.message_thread_id
        )


@limit_usage
async def dfhjbsdhjbfjdsbfsjkhfbsjhfsd(update: Update, context):
    await context.bot.copy_message(
        chat_id=update.effective_chat.id,
        from_chat_id=CHAT_ID,
        message_id=13729,
        message_thread_id=update.message.message_thread_id
    )


@limit_usage
async def schedule(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return
    if update.message:
        await update.message.reply_text(
            'čítali ste kanál <a href="https://t.me/c/2307996875/4/4463">ASAP</a>?',
            parse_mode="HTML"
        )
        await context.bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=4463,
            message_thread_id=update.message.message_thread_id
        )


@limit_usage
async def invite(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return
    if update.message:
        await update.message.reply_text(
            'https://t.me/+oMLyG94WRD85YWIy',
            parse_mode="HTML"
        )


@limit_usage
async def todolist(update: Update, context):
    if update.message.chat.id not in ALLOWED_IDS:
        return
    with (open("config.py", "r", encoding="utf-8") as file):
        for line in file:
            if line.startswith("TODOLIST_ID"):
                todolist_id = int(line.split("=")[1].strip())
    if update.message:
        await context.bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=todolist_id,
            message_thread_id=update.message.message_thread_id
        )


@limit_usage
async def week(update: Update, context):
    now = datetime.now()
    now = now.replace(hour=0, minute=0, second=0, microsecond=0)

    current_week = round((now - SEMESTER_START).days / 7)
    if now.weekday() not in [0, 5, 6]:
        current_week += 1

    if now >= SEMESTER_START:
        message = f"Sme v {current_week}. týždni semestra."
    else:
        message = f"Uvidíme sa {SEMESTER_START.strftime('%d.%m.%Y')}!"

    await update.message.reply_text(message)
