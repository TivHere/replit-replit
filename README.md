# Telegram Cafe Bot

A beautiful and interactive Telegram bot for cafe businesses with welcome photos and text-based menu navigation.

## Features

- **Welcome Photo**: Shows beautiful cafe interior when users start
- **Interactive Menu**: Browse categories with inline keyboards
- **Text-Based Items**: Fast, clean menu item displays
- **Order System**: Phone and email ordering options
- **Contact Info**: Business details and social media links
- **Responsive Design**: Works perfectly on mobile devices

## Setup Instructions

### 1. Get a Telegram Bot Token

1. Open Telegram and search for `@BotFather`
2. Start a chat with BotFather and send `/newbot`
3. Follow the prompts to name your bot (e.g., "My Cafe Bot")
4. Choose a username ending in "bot" (e.g., "mycafebot")
5. Copy the bot token provided by BotFather

### 2. Install Dependencies

```bash
pip install python-telegram-bot==20.7
```

### 3. Set Environment Variable

Set your bot token as an environment variable:

**Linux/Mac:**
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
```

**Windows:**
```cmd
set TELEGRAM_BOT_TOKEN=your_bot_token_here
```

### 4. Customize Your Cafe

Edit `config.py` to update:
- Cafe name and description
- Contact information (phone, email, address)
- Opening hours
- Social media links

Edit `menu_data.json` to update:
- Menu categories and items
- Prices and descriptions
- Cafe photos for welcome screen

### 5. Run the Bot

```bash
python main.py
```

## Bot Commands

- `/start` - Welcome message with cafe photo and main menu
- `/menu` - Browse menu categories
- `/contact` - Get contact information
- `/location` - Address and opening hours
- `/help` - Usage instructions

## File Structure

- `main.py` - Bot entry point and initialization
- `config.py` - Configuration settings and messages
- `handlers.py` - Message and callback handlers
- `utils.py` - Utility functions for keyboards and menus
- `menu_data.json` - Menu items and cafe images
- `pyproject.toml` - Python dependencies

## Customization

### Adding Menu Items

Edit `menu_data.json` to add new categories or items:

```json
{
  "id": "new_item",
  "name": "New Menu Item",
  "description": "Delicious new addition to our menu",
  "price": "$5.99",
  "category": "category_name"
}
```

### Changing Cafe Information

Update `config.py` with your cafe's details:

```python
CAFE_NAME = "Your Cafe Name"
CAFE_PHONE = "+1 (555) 123-4567"
CAFE_EMAIL = "hello@yourcafe.com"
```

### Welcome Photos

Add cafe interior photos to `menu_data.json` in the `cafe_images` array. The bot will randomly select one for the welcome message.

## Support

This bot is designed to be simple and reliable. If you need help:

1. Check that your bot token is correctly set
2. Ensure all dependencies are installed
3. Verify your menu data JSON is valid
4. Check the console logs for error messages

## License

Free to use and modify for your cafe business.