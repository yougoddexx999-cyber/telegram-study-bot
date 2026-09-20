
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
                "🎥 Ethical Hacking",
                callback_data="ethicalhacking"
            ),
            InlineKeyboardButton(
                "💻 Coding",
                callback_data="coding"
            )
        ],
        [
            InlineKeyboardButton(
                "📖 Notes",
                callback_data="notes"
            )
        ],
        [
            InlineKeyboardButton(
                "📝 Practice Questions",
                callback_data="questions"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "📚 Goddy ke bot mein aapka swagat hai!\n\n"
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

    if query.data == "ethicalhacking":

        keyboard = [
            [
                InlineKeyboardButton(
                    "▶️ Ethical Hacking Video 1",
                    url="https://www.youtube.com/watch?v=EZ_bUnO19jk&list=PLKIA7SbSqA4c&pp=0gcJCf8COCosWNinsAgC"
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "🎥 Ethical Hacking Videos\n\n"
            "Neeche video select karo 👇",
            reply_markup=reply_markup
        )


    # ==============================
    # CODING
    # ==============================

    elif query.data == "coding":

        keyboard = [
            [
                InlineKeyboardButton(
                    "▶️ Python 1",
                    url="https://www.youtube.com/watch?v=UrsmFxEIp5k&pp=ygUScHl0aG9uIGZ1bGwgY291cnNl0gcJCSQMAYcqIYzv"
                )
            ],
            [
                InlineKeyboardButton(
                    "▶️ C Language 1",
                    url="https://youtu.be/9xCskNFVt2c?si=VBRJVhAPy92zE5OT"
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "💻 Coding Videos\n\n"
            "Neeche video select karo 👇",
            reply_markup=reply_markup
        )


    # ==============================
    # NOTES
    # ==============================

    elif query.data == "notes":

        await query.message.reply_text(
            "📖 Notes bhej raha hoon..."
        )

        await query.message.reply_document(
            document=open(
                r"C:\Users\Prompt\Downloads\C_Complete_Notes.pdf",
                "rb"
            ),
            caption="📖 C Programming Complete Notes"
        )

        await query.message.reply_document(
            document=open(
                r"C:\Users\Prompt\Downloads\Python_Complete_Notes.pdf",
                "rb"
            ),
            caption="🐍 Python Complete Notes"
        )


    # ==============================
    # PRACTICE QUESTIONS
    # ==============================

    elif query.data == "questions":

        await query.message.reply_text(
            "📝 Practice Questions\n\n"
            "Abhi yahan questions add karenge."
        )


# ==============================
# NORMAL MESSAGE
# ==============================

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    await update.message.reply_text(
        f"Aapne bheja: {text}"
    )


# ==============================
# BOT SETUP
# ==============================

app = Application.builder().token("bot_token").build()

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

