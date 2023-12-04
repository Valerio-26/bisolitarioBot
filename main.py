# ©Bisolitario s.r.l.

from typing import Final
from telegram import *
from telegram.ext import *
import requests

TOKEN: Final = "6562392343:AAGQyrW-wkhsvrqsudgQFZxWAHXdkgus9PU"
BOT_USERNAME: Final = "@BisolitarioBot"


# commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [KeyboardButton("mazzetto")],
        [KeyboardButton("porcodio")],
        [KeyboardButton("ooooo")],
        [KeyboardButton("ooooo")],
        [KeyboardButton("ooooo")],
        [KeyboardButton("ooooo")],
    ]
    await update.message.reply_text("Hello", reply_markup=ReplyKeyboardMarkup(buttons))


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Help try")


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("entrato")
    await update.message.reply_text("boh, custom command")


async def put_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):  # bottone mano
    await update.message.reply_text(
        "put",
        disable_notification=True,
    )


def handle_response(text: str) -> str:
    if "hello" in text:
        return "hello there"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

        print("Bot: ", response)
        await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))
    app.add_handler(CommandHandler("put", put_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print("Polling...")
    app.run_polling(poll_interval=3)
