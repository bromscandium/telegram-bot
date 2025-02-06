from telegram import Update
from telegram.ext import filters


async def welcome(update: Update, context):
    if update.message.new_chat_members:
        for user in update.message.new_chat_members:
            name = user.full_name
            await update.message.reply_text(
                f"Vítam ťa, <b>ledáč {name}</b>.\n\n"
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
