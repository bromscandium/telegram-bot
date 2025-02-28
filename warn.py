import sqlite3
from datetime import datetime, timedelta
from telegram import Update, ChatPermissions
from telegram.ext import CallbackContext

from admin import is_possible_to_use, get_user_from_reply
from config import ADMINS_ID


def create_db():
    conn = sqlite3.connect('warnings.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS warnings (
                    user_id INTEGER PRIMARY KEY,
                    warnings INTEGER DEFAULT 0,
                    reasons TEXT)''')
    conn.commit()
    conn.close()


def add_warning(user_id, reason):
    conn = sqlite3.connect('warnings.db')
    c = conn.cursor()

    c.execute("SELECT warnings, reasons FROM warnings WHERE user_id = ?", (user_id,))
    result = c.fetchone()

    timestamp = datetime.now().strftime("%d.%m %H:%M")
    formatted_reason = f"{timestamp} {reason}"

    if result:
        warnings_count, reasons = result
        new_warning_count = warnings_count + 1
        updated_reasons = reasons + f"\n{formatted_reason}" if reasons else formatted_reason

        c.execute("UPDATE warnings SET warnings = ?, reasons = ? WHERE user_id = ?",
                  (new_warning_count, updated_reasons, user_id))
    else:
        c.execute("INSERT INTO warnings (user_id, warnings, reasons) VALUES (?, ?, ?)",
                  (user_id, 1, formatted_reason))

    conn.commit()
    conn.close()


def get_warning_count(user_id):
    conn = sqlite3.connect('warnings.db')
    c = conn.cursor()
    c.execute("SELECT warnings FROM warnings WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()

    return result[0] if result else 0


def get_warning_reasons(user_id):
    conn = sqlite3.connect('warnings.db')
    c = conn.cursor()
    c.execute("SELECT reasons FROM warnings WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()

    if result and result[0]:
        return result[0]
    return "—"


def reset_warnings(user_id):
    conn = sqlite3.connect('warnings.db')
    c = conn.cursor()
    c.execute("UPDATE warnings SET warnings = 0 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


async def list_warn(update: Update, context):
    if await is_possible_to_use(update) is False:
        return
    user = await get_user_from_reply(update)
    if user is None:
        return

    warnings_count = get_warning_count(user.id)
    reasons = get_warning_reasons(user.id)

    if reasons == "—":
        await update.message.reply_text("Tento ledač nemá žiadne varovania.")
    else:
        await update.message.reply_text(
            f"{user.full_name} má {warnings_count} varovania:\n\n{reasons}"
        )


async def warn(update: Update, context: CallbackContext):
    if await is_possible_to_use(update) is False:
        return
    user = await get_user_from_reply(update)
    if user is None:
        return
    if user.id in ADMINS_ID:
        await update.message.reply_text(f"{user.full_name} je administrátor, nemôže byť umlčaný.")
        return

    reason = ' '.join(context.args) if context.args else 'Bez dôvodu'

    add_warning(user.id, reason)

    warnings_count = get_warning_count(user.id)

    if warnings_count >= 3:
        until_date = update.message.date + timedelta(hours=2)
        restriction = ChatPermissions(can_send_messages=False)
        await context.bot.restrict_chat_member(chat_id=update.effective_chat.id, user_id=user.id,
                                               permissions=restriction, until_date=until_date)
        reset_warnings(user.id)

        await update.message.reply_text(
            f"{user.full_name} dostal {warnings_count} varovaní a bude spat 2 hodiny."
        )
    else:
        await update.message.reply_text(
            f"{user.full_name} dostal varovanie. Teraz má {warnings_count}."
        )


async def unwarn(update: Update, context):
    if await is_possible_to_use(update) is False:
        return
    user = await get_user_from_reply(update)
    if user is None:
        return

    reset_warnings(user.id)

    await update.message.reply_text(
        f"všetky varovania boli vymazané z ledača {user.full_name}."
    )


create_db()
