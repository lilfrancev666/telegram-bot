from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import random

TOKEN = "8535830257:AAH_PZpFGFQadYNmn1H017YYX3jYLW9g7gk"

messages = [
    "Уверенный голос влияет сильнее громкости.",
    "Люди запоминают эмоции, а не слова.",
    "Пауза перед ответом добавляет вес словам.",
    "Умение слушать делает тебя интереснее.",
    "Спокойствие создает ощущение силы."
]

users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    users.add(chat_id)

    await update.message.reply_text(
        "Ежедневные советы активированы 😎"
    )

async def send_daily_messages(app):
    for user in users:
        text = random.choice(messages)

        try:
            await app.bot.send_message(chat_id=user, text=text)
        except:
            pass

async def main():
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

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())