"""
Utility functions for the Enhanced Telegram Cafe Bot
"""

import json
import logging
from typing import Dict, List, Any
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

logger = logging.getLogger(__name__)

def load_menu_data() -> Dict[str, Any]:
    """Load menu data from JSON file"""
    try:
        with open('menu_data.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error("Menu data file not found")
        return {"categories": {}}
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing menu data: {e}")
        return {"categories": {}}

def create_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Create the main menu keyboard with category buttons"""
    menu_data = load_menu_data()
    keyboard = []
    
    # Add category buttons
    for category_key, category_data in menu_data.get("categories", {}).items():
        keyboard.append([
            InlineKeyboardButton(
                category_data["name"], 
                callback_data=f"category_{category_key}"
            )
        ])
    
    # Add additional buttons
    keyboard.extend([
        [InlineKeyboardButton("📞 Contact Info", callback_data="contact")],
        [InlineKeyboardButton("📍 Location & Hours", callback_data="location")],
        [InlineKeyboardButton("📱 Place Order", callback_data="order")]
    ])
    
    return InlineKeyboardMarkup(keyboard)

def create_category_keyboard(category: str) -> InlineKeyboardMarkup:
    """Create keyboard for a specific menu category"""
    menu_data = load_menu_data()
    keyboard = []
    
    category_data = menu_data.get("categories", {}).get(category, {})
    items = category_data.get("items", [])
    
    # Add item buttons (2 per row for better mobile experience)
    for i in range(0, len(items), 2):
        row = []
        for j in range(2):
            if i + j < len(items):
                item = items[i + j]
                row.append(InlineKeyboardButton(
                    f"{item['name']} - {item['price']}", 
                    callback_data=f"item_{item['id']}"
                ))
        keyboard.append(row)
    
    # Add navigation buttons
    keyboard.extend([
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")],
        [InlineKeyboardButton("📱 Place Order", callback_data="order")]
    ])
    
    return InlineKeyboardMarkup(keyboard)

def create_item_keyboard(item_id: str) -> InlineKeyboardMarkup:
    """Create keyboard for a specific menu item"""
    keyboard = [
        [InlineKeyboardButton("📱 Order This Item", callback_data=f"order_{item_id}")],
        [InlineKeyboardButton("🔙 Back to Category", callback_data="back_to_category")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def format_item_message(item: Dict[str, Any]) -> str:
    """Format a menu item message with emoji and styling"""
    return f"""
✨ **{item['name']}** ✨

📝 {item['description']}

💰 **Price:** {item['price']}

Ready to order? Use the buttons below! 👇
"""

def format_category_message(category_key: str) -> str:
    """Format a category overview message"""
    menu_data = load_menu_data()
    category = menu_data.get("categories", {}).get(category_key, {})
    
    message = f"""
{category.get('emoji', '🍽️')} **{category.get('name', 'Menu Category')}** {category.get('emoji', '🍽️')}

{category.get('description', 'Delicious options await!')}

Choose an item below to see details! 👇
"""
    
    return message

def get_item_by_id(item_id: str) -> Dict[str, Any]:
    """Get a menu item by its ID"""
    menu_data = load_menu_data()
    
    for category_data in menu_data.get("categories", {}).values():
        for item in category_data.get("items", []):
            if item.get("id") == item_id:
                return item
    
    return {}

def get_category_by_item_id(item_id: str) -> str:
    """Get the category key for a given item ID"""
    menu_data = load_menu_data()
    
    for category_key, category_data in menu_data.get("categories", {}).items():
        for item in category_data.get("items", []):
            if item.get("id") == item_id:
                return category_key
    
    return ""

def create_order_keyboard() -> InlineKeyboardMarkup:
    """Create keyboard for order information"""
    keyboard = [
        [InlineKeyboardButton("📞 Call to Order", callback_data="call_order")],
        [InlineKeyboardButton("📧 Email Order", callback_data="email_order")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def create_contact_keyboard() -> InlineKeyboardMarkup:
    """Create keyboard for contact information"""
    keyboard = [
        [InlineKeyboardButton("📞 Call Us", callback_data="call_cafe")],
        [InlineKeyboardButton("📧 Email Us", callback_data="email_cafe")],
        [InlineKeyboardButton("🌐 Visit Website", callback_data="website")],
        [InlineKeyboardButton("📱 Instagram", callback_data="instagram")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def create_back_keyboard() -> InlineKeyboardMarkup:
    """Create simple back to menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")]
    ]
    
    return InlineKeyboardMarkup(keyboard)
