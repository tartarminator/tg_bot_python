import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Replace with your actual token
TOKEN = "YOUR-TELEGRAM-BOT-TOKEN"

# Simple menu database
MENU = {
    "☕ Coffee": 2.50,
    "🥐 Cappuccino": 3.00,
    "🥪 Sandwich": 4.50,
    "🥗 Salad": 5.00,
    "🍰 Cake": 3.50
}

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Store user orders
user_orders = {}

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Handle /start command"""
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Menu")],
            [KeyboardButton(text="🛒 Order")],
            [KeyboardButton(text="❓ Help")],
        ],
        resize_keyboard=True,
    )
    await message.answer(
        "Welcome to Our Cafe! ☕\n\nPlease choose an option:",
        reply_markup=kb
    )

@dp.message(lambda msg: msg.text == "📋 Menu")
async def show_menu(message: types.Message):
    """Show the menu"""
    menu_text = "<b>📋 Our Menu:</b>\n\n"
    for item, price in MENU.items():
        menu_text += f"{item} - ${price}\n"
    
    await message.answer(menu_text, parse_mode="HTML")

@dp.message(lambda msg: msg.text == "🛒 Order")
async def start_order(message: types.Message):
    """Start the ordering process"""
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=item)] for item in MENU.keys()
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(
        "What would you like to order?",
        reply_markup=kb
    )

@dp.message(lambda msg: msg.text in MENU)
async def process_order(message: types.Message):
    """Process the selected item"""
    item = message.text
    price = MENU[item]
    user_id = message.from_user.id
    
    # Store order
    if user_id not in user_orders:
        user_orders[user_id] = []
    
    user_orders[user_id].append({"item": item, "price": price})
    
    # Show confirmation
    total = sum(order["price"] for order in user_orders[user_id])
    
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Checkout")],
            [KeyboardButton(text="➕ Add More")],
            [KeyboardButton(text="❌ Cancel")],
        ],
        resize_keyboard=True,
    )
    
    await message.answer(
        f"✅ Added to cart: <b>{item}</b> (${price})\n\n"
        f"<b>Current Total: ${total}</b>",
        reply_markup=kb,
        parse_mode="HTML"
    )

@dp.message(lambda msg: msg.text == "✅ Checkout")
async def checkout(message: types.Message):
    """Process checkout"""
    user_id = message.from_user.id
    
    if user_id not in user_orders or not user_orders[user_id]:
        await message.answer("Your cart is empty!")
        return
    
    total = sum(order["price"] for order in user_orders[user_id])
    order_text = "<b>Your Order:</b>\n"
    
    for order in user_orders[user_id]:
        order_text += f"• {order['item']} - ${order['price']}\n"
    
    order_text += f"\n<b>Total: ${total}</b>\n\n✅ Thank you for your order!\nYour order will be ready in 15-20 minutes."
    
    # Clear user's order
    user_orders[user_id] = []
    
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Menu")],
            [KeyboardButton(text="🛒 Order")],
        ],
        resize_keyboard=True,
    )
    
    await message.answer(order_text, reply_markup=kb, parse_mode="HTML")

@dp.message(lambda msg: msg.text == "❌ Cancel")
async def cancel_order(message: types.Message):
    """Cancel the order"""
    user_id = message.from_user.id
    user_orders[user_id] = []
    
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Menu")],
            [KeyboardButton(text="🛒 Order")],
        ],
        resize_keyboard=True,
    )
    
    await message.answer("Order cancelled. ❌", reply_markup=kb)

@dp.message(lambda msg: msg.text == "❓ Help")
async def help_handler(message: types.Message):
    """Show help"""
    await message.answer(
        "<b>How to use this bot:</b>\n\n"
        "1. Press '📋 Menu' to see our items and prices\n"
        "2. Press '🛒 Order' to start ordering\n"
        "3. Select items you want\n"
        "4. Press '✅ Checkout' to complete your order\n\n"
        "For support, contact us at: @cafe_support",
        parse_mode="HTML"
    )

@dp.message()
async def echo(message: types.Message):
    """Echo handler"""
    await message.answer("I didn't understand that. Please use the menu buttons.")

async def main():
    """Start polling"""
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())