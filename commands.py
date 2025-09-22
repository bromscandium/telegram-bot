import asyncio
import time
from datetime import datetime, timedelta

from telegram import Update

from config import CHAT_ID, ADMIN_CHAT_ID, SEMESTER_START, LINK

message_counter = 0
command_usage = {}
user_last_called = {}


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


def personal_limit_usage(seconds):
    def decorator(func):
        async def wrapper(update: Update, context):
            user_id = update.effective_user.id
            now = time.time()
            last_time = user_last_called.get(user_id, 0)
            if now - last_time < seconds:
                return
            user_last_called[user_id] = now
            await func(update, context)

        return wrapper

    return decorator


# User commands

@limit_usage
async def rules(update: Update, context):
    if update.message:
        await update.message.reply_text(
            'čítali ste kanál <a href="https://t.me/c/2307996875/4/224677">ASAP</a>?',
            parse_mode="HTML"
        )


@limit_usage
async def moodle(update: Update, context):
    if update.message:
        await context.bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=224679,
            message_thread_id=update.message.message_thread_id,
        )


@limit_usage
async def links(update: Update, context):
    if update.message:
        await context.bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=224678,
            message_thread_id=update.message.message_thread_id,
        )


@limit_usage
async def scores(update: Update, context):
    if update.message:
        await update.message.reply_text(
            'Čítali ste kanál <a href="https://t.me/c/2307996875/4/224680">ASAP</a>?',
            parse_mode="HTML"
        )


@limit_usage
async def plan(update: Update, context):
    if update.message:
        await context.bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=224681,
            message_thread_id=update.message.message_thread_id
        )


@limit_usage
async def maptuke(update: Update, context):
    if update.message:
        await context.bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=224682,
            message_thread_id=update.message.message_thread_id
        )


@limit_usage
async def map5p(update: Update, context):
    if update.message:
        await context.bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=224683,
            message_thread_id=update.message.message_thread_id
        )


@limit_usage
async def studijne(update: Update, context):
    if update.message:
        await context.bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=224684,
            message_thread_id=update.message.message_thread_id
        )


@limit_usage
async def schedule(update: Update, context):
    if update.message:
        await context.bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHAT_ID,
            message_id=224685,
            message_thread_id=update.message.message_thread_id
        )


@limit_usage
async def invite(update: Update, context):
    if update.message:
        await update.message.reply_text(LINK)


@limit_usage
async def week(update: Update, context):
    now = datetime.now()

    if now < SEMESTER_START:
        message = f"Semester sa začne {SEMESTER_START.strftime('%d.%m.%Y')}."
    else:
        current_week = ((now - SEMESTER_START).days // 7) + 1
        if current_week <= 13:
            message = f"Sme v {current_week}. týždni semestra."
        else:
            message = "Uvidíme sa neskor"

    await update.message.reply_text(message)