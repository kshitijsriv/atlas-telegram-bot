# Atlas Telegram Bot

This is a simple Telegram bot to play the classic geography-based game, **Atlas**, where players take turns naming places. Each new place must start with the last letter of the previous one. This bot facilitates multiplayer gameplay directly within Telegram, managing turns and keeping track of the game state.

## Features

- **New Game Setup**: Players can start a new game with the `/newgame` command.
- **Join Game**: A second player can join an existing game using the `/join` command.
- **Turn-Based Gameplay**: The bot ensures each player takes turns correctly.
- **Place Validation**: The bot verifies if the place starts with the correct letter and hasn’t been used before.
- **Forfeit Option**: A player can forfeit the game using the `/forfeit` command.
- **Automatic Game End**: The bot declares a winner when the game ends.

## Commands

- `/start`: Start the bot and display a welcome message.
- `/newgame`: Start a new game. Only one game can be active in a chat at a time.
- `/join`: Join an ongoing game. The game requires two players to begin.
- `/forfeit`: Forfeit the game, declaring the other player as the winner.
- **Place Names**: Players can type place names directly, and the bot will verify them based on the game rules.

## How to Play

1. **Start a Game**: One player initiates a game by typing `/newgame`.
2. **Join the Game**: The second player joins the game by typing `/join`.
3. **Play**: The first player will start with a place name starting with the letter "S". The second player must respond with a place name starting with the last letter of the previous place.
4. **Winning**: A player can forfeit with the `/forfeit` command, allowing the other player to win. The game ends automatically after this.

## Installation

### Prerequisites

- Python 3.8+
- A Telegram bot token from [BotFather](https://core.telegram.org/bots#botfather)

### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/kshitijsriv/atlas-telegram-bot.git
   cd atlas-telegram-bot
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set your bot token:
   Create a `.env` file and add your Telegram bot token:
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   ```

5. Run the bot:
   ```bash
   python main.py
   ```