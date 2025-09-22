import random, hashlib
import aiohttp
from datetime import timedelta, datetime

from telegram.ext import CallbackContext

from admin import is_possible
from commands import personal_limit_usage
from config import REACTIONS, CHAT_ID, ADMINS_ID, BLACKLIST, WEATHER_API_KEY
from telegram import Update, ChatPermissions
from database import get_random_prediction

message_counter = 0
next_reaction = random.randint(100, 170)


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
                "👉 Existuje aj Dôležité IRL (<b>Важливе IRL</b> ?) – tam hádžte všetko mimo učenia, nech tu nemáme bordel.\n\n"
                "Uvidíme, či z teba niečo bude, alebo skončíš v tradičnom zozname.",
                parse_mode="HTML"
            )


async def reaction(update: Update, context):
    global message_counter, next_reaction
    if update.message:
        message_counter += 1
        if message_counter >= next_reaction:
            await context.bot.set_message_reaction(
                chat_id=update.message.chat_id,
                message_id=update.message.message_id,
                reaction=random.choice(REACTIONS),
                is_big=False
            )
            message_counter = 0

            next_reaction = random.randint(100, 170)


@personal_limit_usage(12000)
async def bless(update: Update, context):
    boosts = await context.bot.get_user_chat_boosts(chat_id=CHAT_ID, user_id=update.message.from_user.id)
    if (not boosts.boosts) is True:
        await update.message.reply_text('Povoleny len pre boosterov!')
        return

    for blacklisted in BLACKLIST:
        if blacklisted in update.message.from_user.id:
            print("blacklisted")
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

@personal_limit_usage(61)
async def predict(update: Update, context):
    prediction = get_random_prediction()
    await update.message.reply_text(
        f"Dnes máš takéto predpovedanie, {update.effective_user.full_name}:\n"
        f"{prediction}",
        parse_mode="HTML"
    )


async def weather(update: Update, context):
    city = "Kosice"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=sk"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                await update.message.reply_text("Nepodarilo sa načítať počasie. Skús neskôr.")
                return

            data = await resp.json()

    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    description = data["weather"][0]["description"].capitalize()
    humidity = data["main"]["humidity"]
    sunrise = (datetime.fromtimestamp(data["sys"]["sunrise"]) + timedelta(hours=2)).strftime("%H:%M")
    sunset = (datetime.fromtimestamp(data["sys"]["sunset"]) + timedelta(hours=2)).strftime("%H:%M")
    wind = data["wind"]["speed"]
    clouds = data["clouds"]["all"]

    msg = (
        f"Počasie v Košiciach:\n"
        f"{description}\n"
        f"Teplota: {temp}°C (pocitovo {feels_like}°C)\n"
        f"Vlhkosť: {humidity}%\n"
        f"Vietor: {wind} m/s\n"
        f"Oblačnosť: {clouds}%\n\n"
        f"Východ: {sunrise}, Západ: {sunset}"
    )

    await update.message.reply_text(msg)


async def chance(update: Update, context):
    text = (update.message.text or "")
    parts = text.split(maxsplit=1)
    query = parts[1].strip() if len(parts) > 1 else ""

    if query:

        key = hashlib.md5(query.lower().encode("utf-8")).hexdigest()
        num = int(key[:8], 16) % 101
        await update.message.reply_text(f"Šanca pre „{query}“: {num}%")
    else:

        num = random.randint(0, 100)
        await update.message.reply_text(f"Šanca byť gejom: {num}%")


async def goko_4orta(update: Update, context):
    await update.message.reply_text("/goko_4оrta")
