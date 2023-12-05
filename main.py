# ©Bisolitario s.r.l.

from typing import Final
from telegram import *
from telegram.ext import *

from library import Card
import random

TOKEN: Final = "6562392343:AAGQyrW-wkhsvrqsudgQFZxWAHXdkgus9PU"
BOT_USERNAME: Final = "@BisolitarioBot"

Deck = []


def fillDeck(Deck: list):
    num = 1
    suits = ["cuori", "quadri", "fiori", "picche"]
    for i in range(1, 104 + 1):  # 104 carte senza jolly
        # Deck.append(Card.Card(num,suits[num%24]))
        if num < 12:
            num += 1
        else:
            num = 0


def shuffleDeck(Deck: list):
    pass


# commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type: str = update.message.chat.type

    # debug
    print(chat_type)

    buttons = [
        [KeyboardButton("mazzetto", request_user=True)],
        [KeyboardButton("mano", request_contact=True)]
    ]

    # start message
    if chat_type == "private":
        await update.message.reply_text(
            "Ciao, sono @BisolitarioBot, il bot per giocare al gioco Bisolitario!\n\n•Premi /startgame per giocare!"
        )
        return

    # solo in gruppo
    await update.message.reply_text("Hello", reply_markup=ReplyKeyboardMarkup(buttons))


async def new_game_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [KeyboardButton("mischia")]]
    await update.message.reply_text("shuffling", reply_markup=ReplyKeyboardMarkup(buttons))


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Help command try")


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("custom command")
    await update.message.reply_text("boh, custom command")


''' # bottone mano
async def put_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "put",
        disable_notification=True,
    )'''


def handle_response(text: str) -> str:
    processed: str = text.lower()

    # debug
    if "hello" in text:
        return "hello there"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type: str = update.message.chat.type
    text: str = update.message.text
    username = update.message.from_user.username

    #controllo username
    if username == None:
        await update.message.reply_text(
            "Sembra che tu non abbia impostato un username!\nImpostalo nelle impostazioni per giocare!")

    # debug messages
    print(f'User @{username} in {chat_type}: "{text}"')

    if chat_type == "private":
        response: str = handle_response(text)

        # debug
        print("Bot: ", response)

        await update.message.reply_text(response)

    else:
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
            await update.message.reply_text(response)
        else:
            return


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))
    # app.add_handler(CommandHandler("put", put_command))
    app.add_handler(CommandHandler("game", new_game_command))

    # fillDeck(Deck)

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print("Polling...")
    app.run_polling(poll_interval=3)
