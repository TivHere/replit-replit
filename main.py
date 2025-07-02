#!/usr/bin/env python3
"""
Enhanced Telegram Cafe Bot with Visual Menu Displays
Main application entry point
"""

import asyncio
import logging
import os
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

from handlers import (
    start_command,
    menu_command,
    handle_callback_query,
    help_command,
    contact_command,
    location_command
)
from config import BOT_TOKEN

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Main function to run the bot"""
    try:
        # Create application
        application = ApplicationBuilder().token(BOT_TOKEN).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("menu", menu_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("contact", contact_command))
        application.add_handler(CommandHandler("location", location_command))
        
        # Add callback query handler for inline keyboards
        application.add_handler(CallbackQueryHandler(handle_callback_query))
        
        logger.info("Starting Enhanced Cafe Bot...")
        
        # Start the bot with polling
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise

if __name__ == "__main__":
    main()
