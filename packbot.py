

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)


# ==============================
# START COMMAND
# ==============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "🤍all resourses are here",
                callback_data="all resourses"
            ),
        ]
    ]
            
        
    

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "💗💖 Goddy ke bot mein aapka swagat hai!\n\n"
        "Aapko kya chahiye? Neeche select karo 👇",
        reply_markup=reply_markup
    )


# ==============================
# BUTTON HANDLER
# ==============================

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()


    # ==============================
    # ETHICAL HACKING
    # ==============================

    if query.data == "all langs resourses":

        keyboard = [
            [
                InlineKeyboardButton(
                    "❤ love me ",
                    url="https://www.codewithharry.com/notes"
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "🎥 goddy pe bhrosha kro ek click karo \n\n"
            "Neeche link select karo 👇",
            reply_markup=reply_markup
        )


    


   



   


# ==============================
# NORMAL MESSAGE
# ==============================

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    reply = (
        "goddy se love krtey ho to share krna 😊\n\n"
        "or bhi bhut sare aapko yha kuch milega \n\n"
        "hamara motive yhi rhega kii aap sbko more information mile and sath main sab kuch kare ek buildup ki trah team goddy se kuch sikhe aap thats shit"
        
    )

    await update.message.reply_text(reply)


# ==============================
# BOT SETUP
# ==============================

app = Application.builder().token("none").build()

app.add_handler(CommandHandler("start", start))

app.add_handler(CallbackQueryHandler(button))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        message
    )
)


print("Chal gaya bhai kya ab jaan lega...")

app.run_polling()

