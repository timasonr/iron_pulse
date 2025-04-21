# IronPulse Telegram Bot

A Telegram bot designed to manage join requests for private channels. The bot automatically sends welcome messages to users who request to join a channel and provides a customizable interface.

## Features

- Sends customizable welcome messages to users who request to join a channel
- Supports HTML formatting in messages
- Add, show, and clear custom inline buttons
- Easy configuration with commands
- Environment variables for secure configuration

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file based on the `.env.example`:
   ```
   cp .env.example .env
   ```
   
4. Edit the `.env` file and add your actual credentials:
   - `API_TOKEN`: Your Telegram bot token from @BotFather
   - `CHANNEL_ID`: Your private channel ID
   
5. Run the bot:
   ```
   python main.py
   ```

## Bot Commands

- `/edit [message]` - Change the welcome message (supports HTML formatting)
- `/addbutton [text] | [url]` - Add a new button with text and URL
- `/showbuttons` - Show all configured buttons
- `/clearbuttons` - Remove all buttons

## Example

```
/edit Welcome to our channel, {username}! Your request is being processed.

/addbutton Our Website | https://example.com
/addbutton Contact Us | https://t.me/username
```

## Requirements

- Python 3.7+
- aiogram 3.x

## License

MIT
