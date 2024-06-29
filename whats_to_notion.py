from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

token_telegram = os.getenv('TOKEN_TELEGRAM')


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text
    timestamp = update.message.date
    print(f'Received message: {message} at {timestamp}')
    with open('mensajes.txt', 'a') as f:
        f.write(f'{message};{timestamp}\n')


app = ApplicationBuilder().token(token_telegram).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(MessageHandler(filters.Text(), handle_message))

app.run_polling()