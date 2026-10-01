import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")


# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "🤍 All resources are here",
                callback_data="all_resources"
            )
        ]
    ]

    await update.message.reply_text(
        "💗💖 Goddy ke bot mein aapka swagat hai!\n\n"
        "Aapko kya chahiye? Neeche select karo 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# BUTTON HANDLER
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "all_resources":

        keyboard = [
            [
                InlineKeyboardButton(
                    "❤ Love me",
                    url="https://www.codewithharry.com/notes"
                )
            ]
        ]

        await query.message.reply_text(
            "🎥 Goddy pe bharosa karo, ek click karo\n\n"
            "Neeche link select karo 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# NORMAL MESSAGE
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    reply = (
        "Goddy se love karte ho to share karna 😊\n\n"
        "Aur bhi bahut saare resources yahan milenge.\n\n"
        "Hamara motive yahi rahega ki aap sabko more information mile."
    )

    await update.message.reply_text(reply)


# BOT SETUP
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

print("Bot chal gaya!")
app.run_polling()
