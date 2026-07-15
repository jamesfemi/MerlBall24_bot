import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging to help see errors on Railway
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 **Welcome to Easy Word Count Bot!**\n\n"
        "Just send or paste any text here, and I will instantly calculate:\n"
        "• Total Words\n"
        "• Characters (with spaces)\n"
        "• Characters (without spaces)\n\n"
        "Give it a try! Send me some text."
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

# Message handler to process and count the text
async def count_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # Calculate metrics
    words_list = text.split()
    word_count = len(words_list)
    char_with_spaces = len(text)
    char_no_spaces = len(text.replace(" ", "").replace("\n", "").replace("\t", ""))
    
    # Format the response clearly
    response = (
        "📊 **Text Analysis:**\n"
        "-----------------------\n"
        f"📝 **Words:** {word_count}\n"
        f"🔤 **Characters (with spaces):** {char_with_spaces}\n"
        f"🚫 **Characters (no spaces):** {char_no_spaces}"
    )
    
    await update.message.reply_text(response, parse_mode="Markdown")

if __name__ == '__main__':
    # Retrieve token from environment variables (safe for Railway)
    TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    
    if not TOKEN:
        raise ValueError("No TELEGRAM_BOT_TOKEN found in environment variables!")

    # Build and start the bot application
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, count_text))
    
    logging.info("Bot is starting...")
    app.run_polling()
