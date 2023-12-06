# ©Bisolitario s.r.l.

from typing import Final
from telegram import *
from telegram.ext import *

from library import Card as lib
import random

from library import Card
import random

TOKEN: Final = "6562392343:AAGQyrW-wkhsvrqsudgQFZxWAHXdkgus9PU"
BOT_USERNAME: Final = "@BisolitarioBot"

username = None
game_started = False  # la partita inizia quando si scrive /game

Usernames = []  # raccoglitore di giocatori

Deck = []  # mazzo di carte
isDeckFull = False


def fillDeck(Deck):  # riempie il mazzo
    global isDeckFull
    num = 1
    c = 0
    semi = ["cuori", "quadri", "fiori", "picche"]
    seme = semi[c]
    for i in range(1, 105):
        Deck.append(lib.Card(num, semi[c % 4]))
        if num <= 12:
            num += 1
        else:
            num = 1
            c += 1
            seme = semi[c % 4]

    isDeckFull = True


# commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type: str = update.message.chat.type

    # debug
    print(chat_type)

    buttons = [
        [KeyboardButton("mazzetto", request_user=True)],
        [KeyboardButton("mano", request_contact=True)],
    ]

    # start message
    if chat_type == "private":
        await update.message.reply_text(
            "Ciao, sono @BisolitarioBot, il bot per giocare al gioco Bisolitario!\n\n•Premi /startgame per giocare!"
        )
        return

    # solo in gruppo
    await update.message.reply_text("Hello", reply_markup=ReplyKeyboardMarkup(buttons))


# test pulsante
async def test_pulsante(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("Test 1", callback_data="test1")],
        [InlineKeyboardButton("Test 2", callback_data="test2")],
    ]

    await update.message.reply_text(
        "Premi un pulsante", reply_markup=InlineKeyboardMarkup(buttons)
    )


# funzioni pulsanti
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data == "test1":
        # Chiamata alla funzione per mescolare le carte
        # Ad esempio: shuffle_deck()
        await update.callback_query.answer("Test 1 ok!")
    elif data == "test2":
        await update.callback_query.answer("Test 2 ok!")


async def new_game_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global game_started
    buttons = [[KeyboardButton("mischia")]]
    game_started = True  # contollo che il game è iniziato
    if not isDeckFull:
        fillDeck(Deck)  # riempie il mazzo con le carte

    # estraggo una carta random quando scrivo
    card = random.choice(Deck)
    await update.message.reply_text(
        f"{card.number} di {card.suit}", reply_markup=ReplyKeyboardMarkup(buttons)
    )


"""async def new_game_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[KeyboardButton("mischia")]]
    await update.message.reply_text(
        "shuffling", reply_markup=ReplyKeyboardMarkup(buttons)
    )
"""


async def join_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if game_started:
        username = update.message.from_user.username
        print(username)
        if username not in Usernames:
            Usernames.append(username)
            await update.message.reply_text(f"benvenuto in partita {username}")
        else:
            await update.message.reply_text(f"{username} sei già in partita")
    else:
        await update.message.reply_text("la partita non è iniziata")


async def exit_game_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global game_started
    if game_started:
        if update.message.from_user.username in Usernames:
            Usernames.remove(update.message.from_user.username)
            await update.message.reply_text(
                f"{update.message.from_user.username} è uscito dalla partita"
            )
        else:
            await update.message.reply_text(
                "non puoi uscire da una partita in cui non sei entrato"
            )

        if len(Usernames) == 0:
            game_started = False
    else:
        await update.message.reply_text("non puoi uscire da una partita non iniziata")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Help command try")


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("custom command")
    await update.message.reply_text("boh, custom command")


""" # bottone mano
async def put_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "put",
        disable_notification=True,
    )"""


def handle_response(text: str) -> str:
    processed: str = text.lower()

    # debug
    if "hello" in text:
        return "hello there"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global username

    chat_type: str = update.message.chat.type
    text: str = update.message.text

    username = update.message.from_user.username

    # controllo username
    if username == None:
        await update.message.reply_text(
            "Sembra che tu non abbia impostato un username!\nImpostalo nelle impostazioni per giocare!"
        )
    # debug messages
    # print(f'User @{username} in {chat_type}: "{text}"')

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
            return "NOTHING"


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("game", new_game_command))
    app.add_handler(CommandHandler("join", join_command))
    app.add_handler(CommandHandler("exit", exit_game_command))

    # pulsanti
    app.add_handler(CommandHandler("test", test_pulsante))
    app.add_handler(CallbackQueryHandler(handle_button))

    # app.add_handler(CommandHandler("custom", custom_command))
    # app.add_handler(CommandHandler("put", put_command))

    # fillDeck(Deck)
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print("Polling...")
    app.run_polling(poll_interval=3)
