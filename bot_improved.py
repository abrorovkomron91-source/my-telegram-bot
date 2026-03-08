import os
import requests
from telegram import Bot
from telegram.ext import Updater, CommandHandler

# Create required directories
os.makedirs('data', exist_ok=True)

# Load token from environment variable
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Error handling
try:
    if TOKEN is None:
        raise ValueError("Token not found. Please set the TELEGRAM_TOKEN environment variable.")
        
    # Initialize bot and updater
    bot = Bot(token=TOKEN)
    updater = Updater(bot=bot, use_context=True)

    # Admin verification (replace with real admin check logic)
    ADMIN_ID = 123456789  # Replace with the actual admin ID

    def start(update, context):
        user_id = update.effective_user.id
        if user_id != ADMIN_ID:
            update.message.reply_text("You are not authorized to use this bot.")
            return
        update.message.reply_text("Hello! Welcome to the bot.")

    updater.dispatcher.add_handler(CommandHandler('start', start))

    # Start polling
    updater.start_polling()
    updater.idle()
except Exception as e:
    # Handle exceptions
    print(f'An error occurred: {e}')