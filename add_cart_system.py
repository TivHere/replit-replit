"""
Add-to-Cart System - Core Implementation
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class CartManager:
    """Manages user shopping carts"""
    
    def __init__(self):
        # In-memory cart storage (user_id -> cart_data)
        self.carts = {}
    
    def add_item(self, user_id, item_id, quantity=1):
        """Add item to user's cart"""
        cart = self.get_cart(user_id)
        
        if 'items' not in cart:
            cart['items'] = {}
        
        # Add or update item quantity
        if item_id in cart['items']:
            cart['items'][item_id] += quantity
        else:
            cart['items'][item_id] = quantity
        
        # Save cart
        self.carts[user_id] = cart
        return True
    
    def get_cart(self, user_id):
        """Get user's cart"""
        return self.carts.get(user_id, {'items': {}})
    
    def update_quantity(self, user_id, item_id, quantity):
        """Update item quantity in cart"""
        cart = self.get_cart(user_id)
        
        if quantity <= 0:
            # Remove item if quantity is 0
            if item_id in cart.get('items', {}):
                del cart['items'][item_id]
        else:
            cart['items'][item_id] = quantity
        
        self.carts[user_id] = cart
        return True
    
    def clear_cart(self, user_id):
        """Clear user's cart"""
        if user_id in self.carts:
            del self.carts[user_id]
        return True


# Add to Cart Handler Functions
async def add_item_to_cart(self, update, context, item_id: str):
    """Add an item to the user's cart"""
    user_id = update.effective_user.id
    item = self.menu_manager.get_item(item_id)
    
    if not item:
        await update.callback_query.answer("Item not found!")
        return
    
    # Add item to cart
    success = self.cart_manager.add_item(user_id, item_id, 1)
    
    if success:
        await update.callback_query.answer(f"✅ {item['name']} added to cart!")
        
        # Show quantity selection buttons
        keyboard = [
            [
                InlineKeyboardButton("➖", callback_data=f"decrease_{item_id}"),
                InlineKeyboardButton("1", callback_data=f"quantity_{item_id}"),
                InlineKeyboardButton("➕", callback_data=f"increase_{item_id}")
            ],
            [InlineKeyboardButton("🛒 View Cart", callback_data="show_cart")],
            [InlineKeyboardButton("◀️ Continue Shopping", callback_data="show_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        text = f"*{item['name']}* added to cart!\n\n"
        text += f"💰 Price: ${item['price']:.2f}\n"
        text += f"📝 {item['description']}\n\n"
        text += "Adjust quantity or continue shopping:"
        
        await update.callback_query.edit_message_text(
            text, 
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )


async def show_cart(self, update, context):
    """Display the user's cart"""
    user_id = update.effective_user.id
    cart = self.cart_manager.get_cart(user_id)
    
    if not cart or not cart.get('items'):
        text = "🛒 Your cart is empty!\n\nBrowse our menu to add some delicious items."
        keyboard = [[InlineKeyboardButton("🍴 View Menu", callback_data="show_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
        return
    
    text = "🛒 *Your Cart*\n\n"
    total = 0
    keyboard = []
    
    for item_id, quantity in cart['items'].items():
        item = self.menu_manager.get_item(item_id)
        if item:
            item_total = item['price'] * quantity
            total += item_total
            
            text += f"*{item['name']}*\n"
            text += f"💰 ${item['price']:.2f} × {quantity} = ${item_total:.2f}\n\n"
            
            # Add quantity control buttons for each item
            keyboard.append([
                InlineKeyboardButton("➖", callback_data=f"decrease_{item_id}"),
                InlineKeyboardButton(f"{item['name']} ({quantity})", callback_data=f"item_{item_id}"),
                InlineKeyboardButton("➕", callback_data=f"increase_{item_id}")
            ])
    
    text += f"💰 *Total: ${total:.2f}*\n\n"
    
    if total > 0:
        keyboard.append([InlineKeyboardButton("📋 Place Order", callback_data="place_order")])
    
    keyboard.append([InlineKeyboardButton("🍴 Continue Shopping", callback_data="show_menu")])
    keyboard.append([InlineKeyboardButton("🗑️ Clear Cart", callback_data="clear_cart")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.edit_message_text(
        text, 
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def update_cart_quantity(self, update, context, action: str, item_id: str):
    """Update item quantity in cart"""
    user_id = update.effective_user.id
    current_qty = self.cart_manager.get_item_quantity(user_id, item_id)
    
    if action == "increase":
        new_qty = current_qty + 1
    elif action == "decrease":
        new_qty = max(0, current_qty - 1)
    else:
        return
    
    if new_qty == 0:
        self.cart_manager.remove_item(user_id, item_id)
        await update.callback_query.answer("Item removed from cart!")
        await self.show_cart(update, context)
    else:
        self.cart_manager.update_quantity(user_id, item_id, new_qty)
        await update.callback_query.answer(f"Quantity updated to {new_qty}")