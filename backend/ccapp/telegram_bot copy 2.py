import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Replace with your bot token from BotFather
TOKEN = "8163540356:AAEf1srHkcJqUGqanheqW7kaT0Lr_mNLZrY"

DJANGO_API = "http://localhost:8000/api/messages/"  # your Django endpoint

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I am your Construction Company Bot.")

# Handle any incoming message
async def save_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    # For now, we’ll store everything as coming from Telegram -> manager@example.com
    payload = {
        "sender_id": 1, #user.username or f"tg_{user.id}",
        "receiver_id": 2,   # you can replace with real manager email later
        "text": text,
    }

    try:
        r = requests.post(DJANGO_API, json=payload)
        if r.status_code == 201:
            print("✅ Message saved:", payload)
        else:
            print("❌ Failed to save:", r.status_code, r.text)
    except Exception as e:
        print("⚠️ Error sending to Django:", e)

    await update.message.reply_text("📨 Your message has been saved in the system.")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_message))

    print("🤖 Bot is running with polling...")
    app.run_polling()

if __name__ == "__main__":
    main()