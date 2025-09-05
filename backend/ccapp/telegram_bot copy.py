from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Replace with your bot token from BotFather
TOKEN = "8163540356:AAEf1srHkcJqUGqanheqW7kaT0Lr_mNLZrY"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello!!! I am your Construction Company Bot.")

# Simple echo handler
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    print(f"Message from {user.username}: {text}")  # log in console
    await update.message.reply_text(f"You said: {text}")

def main():
    # Create app with polling
    app = Application.builder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run bot
    print("🤖 Bot is polling Telegram...")
    app.run_polling()

if __name__ == "__main__":
    main()
