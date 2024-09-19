import json
import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from check_valid_place_name import is_valid_location, load_valid_places

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

games = {}
VALID_PLACE_CHECK_FLAG = os.getenv("VALID_PLACE_CHECK_FLAG", 'false') == 'true'
VALID_PLACES_NAMES_FILEPATH = os.getenv("VALID_PLACES_NAMES_FILEPATH", 'data/valid_places.json')
load_dotenv('.env')
valid_places = load_valid_places(VALID_PLACES_NAMES_FILEPATH)


# Add a new place to the valid places file
async def add_place(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) > 0:
        place_name = ' '.join(context.args).strip().lower()

        # Load existing places from the JSON file
        with open(VALID_PLACES_NAMES_FILEPATH, 'r') as file:
            places = json.load(file)

        # Check if the place already exists
        if place_name in places:
            await update.message.reply_text(f"Place '{place_name}' is already in the list.")
        else:
            # Add the new place and save the updated list
            places.append(place_name)
            with open(VALID_PLACES_NAMES_FILEPATH, 'w') as file:
                json.dump(places, file)

            # Reload the valid places
            global valid_places
            valid_places = load_valid_places(VALID_PLACES_NAMES_FILEPATH)

            await update.message.reply_text(f"Place '{place_name}' added successfully!")
    else:
        await update.message.reply_text("Please provide a place name.")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome to Atlas! Type /newgame to start a new game.')


async def new_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    player1 = update.effective_user
    games[chat_id] = {
        'last_place': 'Atlas',
        'used_places': set(),
        'players': [player1],
        'current_player': 0
    }
    await update.message.reply_text(
        f'New game started by {player1.first_name}! Waiting for another player to join. Type /join to join the game.')


async def join_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    player2 = update.effective_user

    if chat_id not in games:
        await update.message.reply_text('No active game. Type /newgame to start a new game.')
        return

    if len(games[chat_id]['players']) == 2:
        await update.message.reply_text('Game is already full.')
        return

    if player2 in games[chat_id]['players']:
        await update.message.reply_text('You are already in the game.')
        return

    games[chat_id]['players'].append(player2)
    await update.message.reply_text(
        f'Player 2 ({player2.first_name}) joined! The game begins. {games[chat_id]["players"][0].first_name}, start with a place name beginning with "S".')


async def play(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if chat_id not in games:
        return  # Ignore messages when no game is active

    if len(games[chat_id]['players']) < 2:
        await update.message.reply_text('Waiting for another player to join.')
        return

    player = update.effective_user
    current_player_index = games[chat_id]['current_player']
    current_player = games[chat_id]['players'][current_player_index]

    if player != current_player:
        await update.message.reply_text(f"It's not your turn. It's {current_player.first_name}'s turn.")
        return

    place = update.message.text.strip().title()
    last_place = games[chat_id]['last_place']
    used_places = games[chat_id]['used_places']

    if place[0].lower() != last_place[-1].lower():
        await update.message.reply_text(f'Invalid move. Place must start with "{last_place[-1].upper()}".')
        return

    valid_place_flag = is_valid_location(place.lower())
    if VALID_PLACE_CHECK_FLAG and not valid_place_flag:
        await update.message.reply_text('This place is not a valid country, state, or city. Try another one.')
        return

    if place in used_places:
        await update.message.reply_text('This place has already been used. Try another one.')
        return

    games[chat_id]['last_place'] = place
    games[chat_id]['used_places'].add(place)
    games[chat_id]['current_player'] = 1 - current_player_index  # Switch player

    next_player = games[chat_id]['players'][games[chat_id]['current_player']]
    await update.message.reply_text(
        f'Valid move! {next_player.first_name}, your turn. Next place must start with "{place[-1].upper()}".')


async def forfeit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if chat_id not in games:
        await update.message.reply_text('No active game.')
        return

    player = update.effective_user
    if player not in games[chat_id]['players']:
        await update.message.reply_text('You are not in this game.')
        return

    winner = games[chat_id]['players'][1 - games[chat_id]['players'].index(player)]
    await end_game(update, context, chat_id, winner)


async def end_game(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id: int, winner) -> None:
    await context.bot.send_message(chat_id, f"Game over! {winner.first_name} wins! 🎉")
    await context.bot.send_message(chat_id, f"🥳")
    del games[chat_id]


def main() -> None:
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("newgame", new_game))
    application.add_handler(CommandHandler("join", join_game))
    application.add_handler(CommandHandler("forfeit", forfeit))
    application.add_handler(CommandHandler("addplace", add_place))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, play))

    application.run_polling()


if __name__ == '__main__':
    main()
