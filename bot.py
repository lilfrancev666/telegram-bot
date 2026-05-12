import os
import random
from datetime import time

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

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

async def daily_message(context: ContextTypes.DEFAULT_TYPE):
    for user in users:
        text = random.choice(messages)

        try:
            await context.bot.send_message(
                chat_id=user,
                text=text
            )
        except:
            pass

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

job_queue = app.job_queue

job_queue.run_daily(
    daily_message,
    time=time(hour=1, minute=28)
)

print("Бот работает")

app.run_polling()