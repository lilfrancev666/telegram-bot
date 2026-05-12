import os
import random

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = os.getenv("TOKEN")

messages = [
    "Спокойствие делает человека убедительнее.",
    "Люди ценят внимание больше красивых слов.",
    "Уверенность рождается из практики.",
    "Пауза перед ответом усиливает эффект слов.",
    "Тот, кто умеет слушать, всегда интереснее."
]

users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    users.add(chat_id)

    await update.message.reply_text(
        "Ты подписался на ежедневные сообщения 😎"
    )

async def send_daily_messages(app):
    for user in users:
        text = random.choice(messages)

        try:
            await app.bot.send_message(chat_id=user, text=text)
        except:
            pass

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

scheduler = AsyncIOScheduler()

scheduler.add_job(
    send_daily_messages,
    "cron",
    hour=12,
    minute=0,
    args=[app]
)

scheduler.start()

print("Бот работает")

app.run_polling()