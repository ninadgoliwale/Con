import os
import random
import logging
import asyncio
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
        logger.error(f"Dice error: {e}")
        await update.message.reply_text("❌ Error!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎰 Commands:\n/coin\n/dice")

def main():
    if TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ ERROR: Please set BOT_TOKEN environment variable!")
        print("Go to Render Dashboard → Environment Variables")
        return
    
    # Create application
    app = Application.builder().token(TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("coin", coin))
    app.add_handler(CommandHandler("dice", dice))
    
    print("🤖 Bot is running 24/7 on Render!")
    print("📋 Commands: /coin, /dice")
    
    # Start polling
    app.run_polling()

if __name__ == "__main__":
    main()
