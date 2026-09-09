import os
import random
import logging
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ============================================
# Get token from environment variable
# Set this in Render dashboard
# ============================================
TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
# ============================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

async def coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = random.choice(['Heads', 'Tails'])
    if result == 'Heads':
        await update.message.reply_text("🪙👤 Heads!")
    else:
        await update.message.reply_text("🪙🦅 Tails!")

async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        dice_msg = await update.message.reply_dice(emoji="🎲")
        await asyncio.sleep(2)
        result = dice_msg.dice.value
        dice_emojis = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}
        await update.message.reply_text(f"{dice_emojis[result]} {result}!")
    except Exception as e:
        await update.message.reply_text("❌ Error!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎰 Commands:\n/coin\n/dice")

telegram_app = Application.builder().token(TOKEN).build()
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("coin", coin))
telegram_app.add_handler(CommandHandler("dice", dice))

@app.route('/')
def home():
    return "🤖 Bot is running 24/7!"

if __name__ == "__main__":
    if TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ Set BOT_TOKEN environment variable!")
        exit(1)
    
    # Run bot in background
    import threading
    threading.Thread(target=telegram_app.run_polling).start()
    
    # Run Flask
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
