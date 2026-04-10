import os
import asyncio
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

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
        response = requests.post(DIFY_API_URL, headers=headers, json=payload, timeout=30)
        data = response.json()
        return data.get("answer", "Sorry, I couldn't get a response. Please try again.")
    except Exception as e:
        return f"Nilaation is having trouble connecting. Please try again in a moment."

# === HANDLE /start COMMAND ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! I'm Nilaation, your AI study assistant!\n\n"
        "I specialize in:\n"
        "📚 Academic knowledge (science, math, history...)\n"
        "🌏 Asian & Cambodian education\n"
        "📖 Book summaries & research\n"
        "✏️ Homework help & exam prep\n\n"
        "Ask me anything! I speak English and Khmer. 😊"
    )

# === HANDLE ALL MESSAGES ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.message.from_user.id

    # Show typing indicator
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    # Get response from Nilaation
    response = ask_nilaation(user_message, user_id)

    # Send response back
    await update.message.reply_text(response)

# === MAIN ===
async def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Nilaation Telegram Bot is running...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())
