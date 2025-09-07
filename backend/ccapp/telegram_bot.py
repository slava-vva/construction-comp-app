import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8163540356:AAEf1srHkcJqUGqanheqW7kaT0Lr_mNLZrY"
DJANGO_USERS_API = "http://localhost:8000/api/chat-users/"
DJANGO_MESSAGES_API = "http://localhost:8000/api/messages/"

MANAGER_ID = 2   # fixed receiver for now


def get_or_create_chat_user(username: str) -> int:
    """Search ChatUser by name, if not exist -> create."""
    try:
        # 1. Try to find the user
        r = requests.get(DJANGO_USERS_API, params={"name": username})
        if r.status_code == 200:
            results = r.json()
            if results:  # if found
                return results[0]["id"]

        # 2. Create user if not found
        r = requests.post(DJANGO_USERS_API, json={"name": username})
        if r.status_code in [200, 201]:
            return r.json()["id"]

        print("❌ Failed to get/create ChatUser:", r.status_code, r.text)
        return None
    except Exception as e:
        print("⚠️ Error:", e)
        return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! You are now connected to the system.")


async def save_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    chat_id = update.message.chat.id
    text = update.message.text
    
    # username = f"{user.username} {chat_id}"
    username = f"{user.username}"

    # Get or create ChatUser
    sender_id = get_or_create_chat_user(username)
    if not sender_id:
        await update.message.reply_text("⚠️ Could not register you in the system.")
        return

    payload = {
        "sender_id": sender_id,
        "receiver_id": MANAGER_ID,
        "text": text,
    }

    # Save message in Django
    try:
        r = requests.post(DJANGO_MESSAGES_API, json=payload)
        if r.status_code in [200, 201]:
            print("✅ Message saved:", payload)
        else:
            print("❌ Failed to save message:", r.status_code, r.text)
    except Exception as e:
        print("⚠️ Error sending to Django:", e)

    await update.message.reply_text("📨 Your message has been stored.")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_message))

    print("🤖 Bot is running with polling...")
    app.run_polling()


if __name__ == "__main__":
    main()
