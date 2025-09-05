from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8163540356:AAEf1srHkcJqUGqanheqW7kaT0Lr_mNLZrY"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! 👷 I'm your Construction Company Bot.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"You said: {update.message.text}")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    app.run_polling()

if __name__ == "__main__":
    main()
