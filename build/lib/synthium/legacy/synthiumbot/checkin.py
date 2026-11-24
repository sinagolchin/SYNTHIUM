"""
SynthiumBot's Daily Check-in Routine
Collects qualitative data to feed into the Synthium Transducer.
"""
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters
from . import tone
from . import memory

# Define conversation states
MOVEMENT, CONNECTION, FOCUS, MOOD = range(4)

async def start_checkin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the check-in process."""
    await update.message.reply_text(
        tone.format_text("Let's log today's coordinates.\n\nFirst, what was your kinetic output (movement) today? (e.g., 'I ran 3 miles', 'I rested on the couch')")
    )
    return MOVEMENT

async def ask_connection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['movement'] = update.message.text
    await update.message.reply_text(
        tone.format_text("Transduced.\n\nWhat did you connect with today? Did you experience art, music, or deep conversations?")
    )
    return CONNECTION

async def ask_focus(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['connection'] = update.message.text
    await update.message.reply_text(
        tone.format_text("Logged.\n\nHow was your capacity and focus? Did you feel clear and capable, or distracted and foggy?")
    )
    return FOCUS

async def ask_mood(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['focus'] = update.message.text
    await update.message.reply_text(
        tone.format_text("Recorded.\n\nFinally, what is your internal entropy (mood) right now? Are you calm, chaotic, anxious, or peaceful?")
    )
    return MOOD

async def complete_checkin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['mood'] = update.message.text
    
    movement = context.user_data['movement']
    connection = context.user_data['connection']
    focus = context.user_data['focus']
    mood = context.user_data['mood']
    
    await update.message.reply_text(tone.format_text("Processing your reality tensor..."))
    
    # Bridge to Synthium
    report = memory.log_daily_checkin(movement, connection, focus, mood)
    
    tensor_msg = (
        f"Today's Coordinates mapped to the manifold.\n"
        f"• {report['summary']}\n\n"
        f"Synthium Projection:\n"
        f"• Enjoyment (E): {report['enjoyment']:.2f}\n"
        f"• Meaning (M): {report['meaning']:.2f}"
    )
    await update.message.reply_text(tensor_msg)
    await update.message.reply_text(tone.get_farewell(report['enjoyment']))
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(tone.format_text("Transduction cancelled. I will remain on standby."))
    return ConversationHandler.END

def get_checkin_handler() -> ConversationHandler:
    """Returns the ConversationHandler to be added to the main app."""
    return ConversationHandler(
        entry_points=[CommandHandler("checkin", start_checkin)],
        states={
            MOVEMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_connection)],
            CONNECTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_focus)],
            FOCUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_mood)],
            MOOD: [MessageHandler(filters.TEXT & ~filters.COMMAND, complete_checkin)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )


