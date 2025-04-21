import logging
import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatJoinRequest, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode

# Load environment variables from .env file
load_dotenv()

# Get configuration from environment variables
API_TOKEN = os.getenv("API_TOKEN", "YOUR_BOT_TOKEN_HERE")
CHANNEL_ID = os.getenv("CHANNEL_ID", "YOUR_CHANNEL_ID_HERE")
WELCOME_MESSAGE = "Hello, {username}! Your request to join the channel has been received! ⏳ Please wait for approval."

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

custom_welcome_message = WELCOME_MESSAGE  # Variable to store custom message
custom_buttons = []  # List to store buttons

def get_welcome_message(username):
    return custom_welcome_message.replace("{username}", username)

def create_keyboard():
    if not custom_buttons:
        return None
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    row = []
    for i, button in enumerate(custom_buttons):
        text, url = button
        row.append(InlineKeyboardButton(text=text, url=url))
        if len(row) == 2 or i == len(custom_buttons) - 1:  # Create rows with 2 buttons
            keyboard.inline_keyboard.append(row)
            row = []
    return keyboard

@dp.chat_join_request()
async def handle_join_request(event: ChatJoinRequest):
    user_id = event.from_user.id
    username = event.from_user.first_name

    try:
        # Send a message to the user with buttons
        await bot.send_message(
            user_id,
            get_welcome_message(username),
            parse_mode=ParseMode.HTML,
            reply_markup=create_keyboard()
        )
        logging.info(f"Message sent to user {username} ({user_id})")
    
    except Exception as e:
        logging.warning(f"Error sending message to {user_id}: {e}")

@dp.message(Command("edit"))
async def edit_welcome_message(message: types.Message):
    global custom_welcome_message
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        await message.reply(
            "Usage: /edit New welcome message\n"
            "To add links use HTML markup, for example:\n"
            "<a href='https://example.com'>Link text</a>"
        )
        return
    
    custom_welcome_message = args[1]
    await message.reply("Welcome message updated!")

@dp.message(Command("addbutton"))
async def add_button(message: types.Message):
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        await message.reply(
            "Usage: /addbutton Button text | URL\n"
            "Example: /addbutton Our channel | https://t.me/channel"
        )
        return
    
    try:
        button_text, button_url = args[1].split("|")
        button_text = button_text.strip()
        button_url = button_url.strip()
        
        custom_buttons.append((button_text, button_url))
        await message.reply(f"Button '{button_text}' added!")
    except ValueError:
        await message.reply("Invalid format. Usage: /addbutton Button text | URL")

@dp.message(Command("clearbuttons"))
async def clear_buttons(message: types.Message):
    global custom_buttons
    custom_buttons = []
    await message.reply("All buttons have been removed!")

@dp.message(Command("showbuttons"))
async def show_buttons(message: types.Message):
    if not custom_buttons:
        await message.reply("Button list is empty!")
        return
    
    buttons_list = "\n".join([f"📌 {text} -> {url}" for text, url in custom_buttons])
    await message.reply(f"Current buttons:\n{buttons_list}")

async def main():
    logging.basicConfig(level=logging.INFO)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
