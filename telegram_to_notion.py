from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from tokenprivado import token_telegram, token_notion, token_page, token_database
from notion_client import Client

client = Client(auth=token_notion)

def write_row(client, database_id, message, timestamp):
    tipo, desc = message.split(',', 1)
    client.pages.create(
        parent={"database_id": database_id},
        properties={
            "Descripcion": {
                "rich_text": [
                    {
                        "text": {
                            "content": desc
                        }
                    }
                ]
            },
            "Tipo": {
                "select": 
                    {
                        "name": tipo
                    }
            },
            "Timestamp": {
                "title": [
                    {
                        "text": {
                            "content": str(timestamp)
                        }
                    }
                ]
            }
        }
    )

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text
    timestamp = update.message.date
    print(f'Received message: {message} at {timestamp}')
    write_row(client, token_database, message, timestamp)

def main():
    app = ApplicationBuilder().token(token_telegram).build()

    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(MessageHandler(filters.Text(), handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()