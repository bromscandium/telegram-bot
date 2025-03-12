import asyncio
from datetime import datetime

from telegram import Update

from config import CHAT_ID, ADMIN_CHAT_ID, SEMESTER_START, LINK

message_counter = 0
command_usage = {}


# Helpful commands

def limit_usage(func):
    async def wrapper(update: Update, context):
        user_id = update.effective_user.id
        command = func.__name__

        usage = command_usage.setdefault(user_id, {}).setdefault(command, 0)

        if usage >= 2:
            return

        command_usage[user_id][command] += 1
        asyncio.create_task(reset_command_usage(user_id, command))
        await func(update, context)

    return wrapper


async def reset_command_usage(user_id: int, command: str):
    await asyncio.sleep(300)
    if user_id in command_usage and command in command_usage[user_id]:
        command_usage[user_id][command] -= 1
        if command_usage[user_id][command] <= 0:
            del command_usage[user_id][command]
        if not command_usage[user_id]:
            del command_usage[user_id]


# User commands

@limit_usage
async def help(update: Update, context):
    if update.message:
        await context.bot.copy_message(
            chat_id=update.effective_chat.id,
            from_chat_id=ADMIN_CHAT_ID,
            message_id=12066,
            message_thread_id=update.message.message_thread_id,
        )


@limit_usage
async def rules(update: Update, context):
    if update.message:
        await update.message.reply_text(
            'čítali ste kanál <a href="https://t.me/c/2307996875/4/52">ASAP</a>?',
            parse_mode="HTML"
        )


@limit_usage
async def moodle(update: Update, context):
    if update.message:
        await context.bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=56,
            message_thread_id=update.message.message_thread_id,
        )


@limit_usage
async def links(update: Update, context):
    if update.message:
        await context.bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=57,
            message_thread_id=update.message.message_thread_id,
        )


@limit_usage
async def scores(update: Update, context):
    if update.message:
        await update.message.reply_text(
            'Čítali ste kanál <a href="https://t.me/c/2307996875/4/63">ASAP</a>?',
            parse_mode="HTML"
        )


@limit_usage
async def plan(update: Update, context):
    if update.message:
        await context.bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=67,
            message_thread_id=update.message.message_thread_id
        )


@limit_usage
async def maptuke(update: Update, context):
    if update.message:
        await context.bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=68,
            message_thread_id=update.message.message_thread_id
        )


@limit_usage
async def map5p(update: Update, context):
    if update.message:
        await context.bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=69,
            message_thread_id=update.message.message_thread_id
        )


@limit_usage
async def studijne(update: Update, context):
    if update.message:
        await context.bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=72,
            message_thread_id=update.message.message_thread_id
        )


@limit_usage
async def schedule(update: Update, context):
    if update.message:
        await context.bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=4463,
            message_thread_id=update.message.message_thread_id
        )


@limit_usage
async def invite(update: Update, context):
    if update.message:
        await update.message.reply_text(LINK)


@limit_usage
async def week(update: Update, context):
    now = datetime.now()
    current_week = ((now - SEMESTER_START).days // 7) + 1 if now >= SEMESTER_START else None

    if current_week:
        message = f"Sme v {current_week}. týždni semestra."
    else:
        message = f"Uvidíme sa {SEMESTER_START.strftime('%d.%m.%Y')}!"

    await update.message.reply_text(message)
