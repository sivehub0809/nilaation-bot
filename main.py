import os
import asyncio
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
from telegram.request import HTTPXRequest

# === CONFIG ===
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
DIFY_API_KEY = os.environ.get("DIFY_API_KEY")
DIFY_API_URL = "https://api.dify.ai/v1/chat-messages"

# === SEND MESSAGE TO DIFY (NILAATION) ===
def ask_nilaation(user_message: str, user_id: str) -> str:
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": {},
        "query": user_message,
        "response_mode": "blocking",
        "user": str(user_id)
    }
    try:
        response = requests.post(DIFY_API_URL, headers=headers, json=payload, timeout=30)
        data = response.json()
        return data.get("answer") or data.get("text") or "Sorry, I couldn't get a response."
    except Exception as e:
        return f"Nilaation is having trouble connecting."

# === HANDLE /start COMMAND ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! I'm Nilaation, your AI study assistant!\n\n"
        "Ask me anything! I speak English and Khmer. 😊"
    )

# === HANDLE ALL MESSAGES ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.message.from_user.id
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    answer = ask_nilaation(user_message, user_id)
    await update.message.reply_text(answer)

# === MAIN ===
async def main():
    # This part stops the "TimedOut" crash you saw in your logs
    request_config = HTTPXRequest(connect_timeout=60, read_timeout=60)
    
    app = Application.builder().token(TELEGRAM_TOKEN).request(request_config).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Nilaation Telegram Bot is running...")
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())
