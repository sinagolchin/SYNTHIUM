import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from . import config
from . import checkin
from . import tone

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    user = update.effective_user
    welcome_text = tone.format_text(
        f"System active. Welcome, {user.first_name}.\n\n"
        "I am SynthiumBot — your personal manifold transducer.\n"
        "We will track your kinetic output, resonance, capacity, and entropy.\n\n"
        "Type /checkin when you are ready to log your coordinates."
    )
    await update.message.reply_text(welcome_text)

def main() -> None:
    """Initialize and start the Telegram bot."""
    app = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    
    # Add SynthiumBot's Conversation Handler
    app.add_handler(checkin.get_checkin_handler())

    logger.info("SynthiumBot is running. Waiting for incoming tensors...")
    app.run_polling()

if __name__ == '__main__':
    main()


