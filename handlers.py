"""
Message and callback handlers for the Enhanced Telegram Cafe Bot
"""

import logging
import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from config import (
    WELCOME_MESSAGE, HELP_MESSAGE, CAFE_PHONE, CAFE_EMAIL, 
    CAFE_ADDRESS, CAFE_HOURS, CAFE_WEBSITE, CAFE_INSTAGRAM,
    ORDER_PHONE, ORDER_EMAIL, CAFE_NAME
)
from utils import (
    load_menu_data, create_main_menu_keyboard, create_category_keyboard,
    create_item_keyboard, format_item_message, format_category_message,
    get_item_by_id, get_category_by_item_id, create_order_keyboard,
    create_contact_keyboard, create_back_keyboard
)

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command with welcome message and cafe interior photo"""
    try:
        menu_data = load_menu_data()
        cafe_images = menu_data.get("cafe_images", [])
        
        # Send a random cafe interior photo with welcome message
        if cafe_images:
            photo_url = random.choice(cafe_images)
            await update.message.reply_photo(
                photo=photo_url,
                caption=WELCOME_MESSAGE,
                reply_markup=create_main_menu_keyboard(),
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            # Fallback if no images available
            await update.message.reply_text(
                WELCOME_MESSAGE,
                reply_markup=create_main_menu_keyboard(),
                parse_mode=ParseMode.MARKDOWN
            )
            
    except Exception as e:
        logger.error(f"Error in start_command: {e}")
        await update.message.reply_text(
            "Welcome to our cafe! 🎉\nSomething went wrong, but we're here to help!",
            reply_markup=create_main_menu_keyboard()
        )

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /menu command"""
    try:
        message = """
🍽️ **Our Menu** 🍽️

Explore our delicious offerings by category:
• Fresh coffee and specialty drinks
• Hearty meals and light bites  
• Sweet pastries and desserts

Choose a category to see our full selection!
"""
        
        await update.message.reply_text(
            message,
            reply_markup=create_main_menu_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
        
    except Exception as e:
        logger.error(f"Error in menu_command: {e}")
        await update.message.reply_text(
            "Here's our menu! 🍽️",
            reply_markup=create_main_menu_keyboard()
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    try:
        await update.message.reply_text(
            HELP_MESSAGE,
            reply_markup=create_back_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
        
    except Exception as e:
        logger.error(f"Error in help_command: {e}")
        await update.message.reply_text(
            "Here's how to use this bot! 🤖",
            reply_markup=create_back_keyboard()
        )

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /contact command"""
    try:
        contact_message = f"""
📞 **Contact {CAFE_NAME}** 📞

**Phone:** {CAFE_PHONE}
**Email:** {CAFE_EMAIL}
**Website:** {CAFE_WEBSITE}
**Instagram:** {CAFE_INSTAGRAM}

**Address:**
{CAFE_ADDRESS}

We'd love to hear from you! 💌
"""
        
        await update.message.reply_text(
            contact_message,
            reply_markup=create_contact_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
        
    except Exception as e:
        logger.error(f"Error in contact_command: {e}")
        await update.message.reply_text(
            f"📞 Contact us at {CAFE_PHONE} or {CAFE_EMAIL}",
            reply_markup=create_back_keyboard()
        )

async def location_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /location command"""
    try:
        location_message = f"""
📍 **Find {CAFE_NAME}** 📍

**Address:**
{CAFE_ADDRESS}

{CAFE_HOURS}

🚗 Parking available
🚌 Public transit accessible
♿ Wheelchair accessible

See you soon! ✨
"""
        
        await update.message.reply_text(
            location_message,
            reply_markup=create_back_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
        
    except Exception as e:
        logger.error(f"Error in location_command: {e}")
        await update.message.reply_text(
            f"📍 Visit us at {CAFE_ADDRESS}",
            reply_markup=create_back_keyboard()
        )

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle all callback queries from inline keyboards"""
    try:
        query = update.callback_query
        await query.answer()
        
        callback_data = query.data
        
        if callback_data == "main_menu":
            await handle_main_menu(query)
        elif callback_data.startswith("category_"):
            category = callback_data.replace("category_", "")
            await handle_category_selection(query, category)
        elif callback_data.startswith("item_"):
            item_id = callback_data.replace("item_", "")
            await handle_item_selection(query, item_id)
        elif callback_data == "back_to_category":
            await handle_back_to_category(query, context)
        elif callback_data == "contact":
            await handle_contact_info(query)
        elif callback_data == "location":
            await handle_location_info(query)
        elif callback_data == "order":
            await handle_order_info(query)
        elif callback_data.startswith("order_"):
            item_id = callback_data.replace("order_", "")
            await handle_order_item(query, item_id)
        elif callback_data == "call_order":
            await handle_call_order(query)
        elif callback_data == "email_order":
            await handle_email_order(query)
        elif callback_data == "call_cafe":
            await handle_call_cafe(query)
        elif callback_data == "email_cafe":
            await handle_email_cafe(query)
        elif callback_data == "website":
            await handle_website(query)
        elif callback_data == "instagram":
            await handle_instagram(query)
            
    except Exception as e:
        logger.error(f"Error in handle_callback_query: {e}")
        try:
            # Try to send a new message instead of editing if editing fails
            await query.message.reply_text("Something went wrong! Use /start to restart the bot.")
        except:
            logger.error("Failed to send error message")

async def handle_main_menu(query) -> None:
    """Handle main menu callback"""
    try:
        main_menu_text = """
🍽️ **Welcome to Our Menu!** 🍽️

Choose a category below to explore our delicious offerings:

✨ Fresh ingredients, made with love
💫 Perfect for dine-in, takeout, or delivery
🎯 Quality food at great prices
"""
        
        # Check if current message has a photo
        if query.message.photo:
            # If it's a photo message, edit the caption
            await query.edit_message_caption(
                caption=main_menu_text,
                reply_markup=create_main_menu_keyboard(),
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            # If it's a text message, edit the text
            await query.edit_message_text(
                main_menu_text,
                reply_markup=create_main_menu_keyboard(),
                parse_mode=ParseMode.MARKDOWN
            )
            
    except Exception as e:
        logger.error(f"Error in handle_main_menu: {e}")
        # Fallback: delete current message and send a new one
        try:
            await query.message.delete()
            await query.message.chat.send_message(
                "🍽️ **Our Menu** 🍽️\n\nChoose a category:",
                reply_markup=create_main_menu_keyboard(),
                parse_mode=ParseMode.MARKDOWN
            )
        except:
            pass

async def handle_category_selection(query, category: str) -> None:
    """Handle category selection"""
    try:
        category_message = format_category_message(category)
        
        # Check if current message has a photo
        if query.message.photo:
            # Delete photo message and send new text message
            await query.message.delete()
            await query.message.chat.send_message(
                category_message,
                reply_markup=create_category_keyboard(category),
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            # Edit text message
            await query.edit_message_text(
                category_message,
                reply_markup=create_category_keyboard(category),
                parse_mode=ParseMode.MARKDOWN
            )
        
    except Exception as e:
        logger.error(f"Error in handle_category_selection: {e}")
        try:
            await query.message.delete()
            await query.message.chat.send_message(
                f"Category: {category.title()}",
                reply_markup=create_category_keyboard(category)
            )
        except:
            pass

async def handle_item_selection(query, item_id: str) -> None:
    """Handle menu item selection without photo"""
    try:
        item = get_item_by_id(item_id)
        
        if not item:
            # Check if current message has a photo
            if query.message.photo:
                await query.message.delete()
                await query.message.chat.send_message(
                    "Sorry, this item is not available.",
                    reply_markup=create_back_keyboard()
                )
            else:
                await query.edit_message_text(
                    "Sorry, this item is not available.",
                    reply_markup=create_back_keyboard()
                )
            return
        
        item_message = format_item_message(item)
        item_keyboard = create_item_keyboard(item_id)
        
        # Always show as text message, no photos for menu items
        if query.message.photo:
            # Delete photo message and send new text message
            await query.message.delete()
            await query.message.chat.send_message(
                item_message,
                reply_markup=item_keyboard,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            # Edit text message
            await query.edit_message_text(
                item_message,
                reply_markup=item_keyboard,
                parse_mode=ParseMode.MARKDOWN
            )
            
    except Exception as e:
        logger.error(f"Error in handle_item_selection: {e}")
        item = get_item_by_id(item_id)
        fallback_message = f"**{item.get('name', 'Menu Item')}**\n\nPrice: {item.get('price', 'N/A')}"
        try:
            if query.message.photo:
                await query.message.delete()
                await query.message.chat.send_message(
                    fallback_message,
                    reply_markup=create_item_keyboard(item_id),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await query.edit_message_text(
                    fallback_message,
                    reply_markup=create_item_keyboard(item_id),
                    parse_mode=ParseMode.MARKDOWN
                )
        except:
            pass

async def handle_back_to_category(query, context) -> None:
    """Handle back to category navigation"""
    try:
        main_menu_text = "🍽️ **Our Menu** 🍽️\n\nChoose a category:"
        
        # Check if current message has a photo
        if query.message.photo:
            # Delete photo message and send new text message
            await query.message.delete()
            await query.message.chat.send_message(
                main_menu_text,
                reply_markup=create_main_menu_keyboard(),
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            # Edit text message
            await query.edit_message_text(
                main_menu_text,
                reply_markup=create_main_menu_keyboard(),
                parse_mode=ParseMode.MARKDOWN
            )
        
    except Exception as e:
        logger.error(f"Error in handle_back_to_category: {e}")
        await handle_main_menu(query)

async def handle_contact_info(query) -> None:
    """Handle contact information display"""
    try:
        contact_message = f"""
📞 **Contact {CAFE_NAME}** 📞

**Phone:** {CAFE_PHONE}
**Email:** {CAFE_EMAIL}
**Website:** {CAFE_WEBSITE}
**Instagram:** {CAFE_INSTAGRAM}

**Address:**
{CAFE_ADDRESS}

We'd love to hear from you! 💌
"""
        
        # Check if current message has a photo
        if query.message.photo:
            # Delete photo message and send new text message
            await query.message.delete()
            await query.message.chat.send_message(
                contact_message,
                reply_markup=create_contact_keyboard(),
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            # Edit text message
            await query.edit_message_text(
                contact_message,
                reply_markup=create_contact_keyboard(),
                parse_mode=ParseMode.MARKDOWN
            )
        
    except Exception as e:
        logger.error(f"Error in handle_contact_info: {e}")
        try:
            await query.message.delete()
            await query.message.chat.send_message(
                f"📞 Contact us at {CAFE_PHONE}",
                reply_markup=create_back_keyboard()
            )
        except:
            pass

async def handle_location_info(query) -> None:
    """Handle location and hours information"""
    try:
        location_message = f"""
📍 **Find {CAFE_NAME}** 📍

**Address:**
{CAFE_ADDRESS}

{CAFE_HOURS}

🚗 Parking available
🚌 Public transit accessible  
♿ Wheelchair accessible

See you soon! ✨
"""
        
        await query.edit_message_text(
            location_message,
            reply_markup=create_back_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
        
    except Exception as e:
        logger.error(f"Error in handle_location_info: {e}")
        await query.edit_message_text(
            f"📍 Visit us at {CAFE_ADDRESS}",
            reply_markup=create_back_keyboard()
        )

async def handle_order_info(query) -> None:
    """Handle order information and options"""
    try:
        order_message = f"""
📱 **Ready to Order?** 📱

**Call to Order:**
📞 {ORDER_PHONE}

**Email Your Order:**
📧 {ORDER_EMAIL}

**Order Information:**
• Please specify items and quantities
• Include your contact information
• Mention pickup or delivery preference
• We'll confirm your order promptly!

🎉 Thank you for choosing {CAFE_NAME}!
"""
        
        await query.edit_message_text(
            order_message,
            reply_markup=create_order_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
        
    except Exception as e:
        logger.error(f"Error in handle_order_info: {e}")
        await query.edit_message_text(
            f"📱 Call {ORDER_PHONE} to place your order!",
            reply_markup=create_back_keyboard()
        )

async def handle_order_item(query, item_id: str) -> None:
    """Handle ordering a specific item"""
    try:
        item = get_item_by_id(item_id)
        
        order_message = f"""
📱 **Order: {item.get('name', 'Item')}** 📱

**Price:** {item.get('price', 'N/A')}

**To place your order:**

📞 **Call:** {ORDER_PHONE}
📧 **Email:** {ORDER_EMAIL}

**Please mention:**
• Item: {item.get('name', 'Item')}
• Quantity desired
• Your contact information
• Pickup or delivery preference

We'll have your order ready! 🎉
"""
        
        await query.edit_message_text(
            order_message,
            reply_markup=create_order_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
        
    except Exception as e:
        logger.error(f"Error in handle_order_item: {e}")
        await query.edit_message_text(
            f"📱 Call {ORDER_PHONE} to order this item!",
            reply_markup=create_back_keyboard()
        )

async def handle_call_order(query) -> None:
    """Handle call to order action"""
    await query.edit_message_text(
        f"📞 **Call to Order**\n\n{ORDER_PHONE}\n\nTap the number to call on mobile devices!",
        reply_markup=create_back_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def handle_email_order(query) -> None:
    """Handle email order action"""
    await query.edit_message_text(
        f"📧 **Email Your Order**\n\n{ORDER_EMAIL}\n\nSend us your order details and we'll get back to you!",
        reply_markup=create_back_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def handle_call_cafe(query) -> None:
    """Handle call cafe action"""
    await query.edit_message_text(
        f"📞 **Call Us**\n\n{CAFE_PHONE}\n\nTap the number to call on mobile devices!",
        reply_markup=create_contact_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def handle_email_cafe(query) -> None:
    """Handle email cafe action"""
    await query.edit_message_text(
        f"📧 **Email Us**\n\n{CAFE_EMAIL}\n\nWe'd love to hear from you!",
        reply_markup=create_contact_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def handle_website(query) -> None:
    """Handle website link"""
    await query.edit_message_text(
        f"🌐 **Visit Our Website**\n\n{CAFE_WEBSITE}\n\nDiscover more about our story and offerings!",
        reply_markup=create_contact_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def handle_instagram(query) -> None:
    """Handle Instagram link"""
    await query.edit_message_text(
        f"📱 **Follow Us on Instagram**\n\n{CAFE_INSTAGRAM}\n\nSee our latest creations and cafe life!",
        reply_markup=create_contact_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )
