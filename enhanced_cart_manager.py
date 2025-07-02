"""
Enhanced Shopping cart management for the Telegram Cafe Bot
Handles user cart operations and storage
"""

import json
import logging
from datetime import datetime
from enhanced_config import MAX_CART_ITEMS

logger = logging.getLogger(__name__)

class CartManager:
    """Manages user shopping carts"""
    
    def __init__(self):
        # In-memory cart storage (user_id -> cart_data)
        # In production, you might want to use Redis or database
        self.carts = {}
    
    def get_cart(self, user_id):
        """Get user's cart"""
        try:
            return self.carts.get(user_id, {
                'items': {},
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            })
        except Exception as e:
            logger.error(f"Error getting cart for user {user_id}: {e}")
            return {'items': {}}
    
    def add_item(self, user_id, item_id, quantity=1):
        """Add item to user's cart"""
        try:
            cart = self.get_cart(user_id)
            
            # Initialize cart if needed
            if 'items' not in cart:
                cart['items'] = {}
            
            # Add or update item quantity
            if item_id in cart['items']:
                cart['items'][item_id] += quantity
            else:
                cart['items'][item_id] = quantity
            
            # Check cart limits
            if len(cart['items']) > MAX_CART_ITEMS:
                logger.warning(f"Cart limit exceeded for user {user_id}")
                return False
            
            # Update timestamps
            cart['updated_at'] = datetime.now().isoformat()
            if 'created_at' not in cart:
                cart['created_at'] = datetime.now().isoformat()
            
            # Save cart
            self.carts[user_id] = cart
            
            logger.info(f"Added item {item_id} (qty: {quantity}) to cart for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding item to cart for user {user_id}: {e}")
            return False
    
    def remove_item(self, user_id, item_id):
        """Remove item from user's cart"""
        try:
            cart = self.get_cart(user_id)
            
            if 'items' in cart and item_id in cart['items']:
                del cart['items'][item_id]
                cart['updated_at'] = datetime.now().isoformat()
                self.carts[user_id] = cart
                
                logger.info(f"Removed item {item_id} from cart for user {user_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error removing item from cart for user {user_id}: {e}")
            return False
    
    def update_quantity(self, user_id, item_id, quantity):
        """Update item quantity in cart"""
        try:
            if quantity <= 0:
                return self.remove_item(user_id, item_id)
            
            cart = self.get_cart(user_id)
            
            if 'items' in cart:
                cart['items'][item_id] = quantity
                cart['updated_at'] = datetime.now().isoformat()
                self.carts[user_id] = cart
                
                logger.info(f"Updated item {item_id} quantity to {quantity} for user {user_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error updating quantity for user {user_id}: {e}")
            return False
    
    def get_item_quantity(self, user_id, item_id):
        """Get quantity of specific item in cart"""
        try:
            cart = self.get_cart(user_id)
            return cart.get('items', {}).get(item_id, 0)
        except Exception as e:
            logger.error(f"Error getting item quantity for user {user_id}: {e}")
            return 0
    
    def clear_cart(self, user_id):
        """Clear user's cart"""
        try:
            if user_id in self.carts:
                del self.carts[user_id]
                logger.info(f"Cleared cart for user {user_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error clearing cart for user {user_id}: {e}")
            return False
    
    def get_cart_total(self, user_id, menu_items):
        """Calculate total price of items in cart"""
        try:
            cart = self.get_cart(user_id)
            total = 0
            
            for item_id, quantity in cart.get('items', {}).items():
                # Find item in menu
                for category, items in menu_items.items():
                    if isinstance(items, dict):
                        for item in items:
                            if item.get('id') == item_id:
                                price = float(item.get('price', '0').replace('$', ''))
                                total += price * quantity
                                break
            
            return total
            
        except Exception as e:
            logger.error(f"Error calculating cart total for user {user_id}: {e}")
            return 0
    
    def get_cart_item_count(self, user_id):
        """Get total number of items in cart"""
        try:
            cart = self.get_cart(user_id)
            return sum(cart.get('items', {}).values())
        except Exception as e:
            logger.error(f"Error getting cart item count for user {user_id}: {e}")
            return 0
    
    def is_cart_empty(self, user_id):
        """Check if cart is empty"""
        try:
            cart = self.get_cart(user_id)
            return len(cart.get('items', {})) == 0
        except Exception as e:
            logger.error(f"Error checking if cart is empty for user {user_id}: {e}")
            return True