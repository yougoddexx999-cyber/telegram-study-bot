
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
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")


# =========================================================
# DUMMY USER DATA
# =========================================================

user_data = {}


# =========================================================
# OWNER PROFILE
# =========================================================

async def ownersprofile(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👑 OWNER PROFILE\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "👤 Name: goddex\n"
        "📧 Email: yougoddexx.com\n"
        "📱 Phone: +91 xxxxxxxxxx\n"
        "🎂 Age: 19\n"
        "🎓 College: almors diploma college\n"
        "📍 State: Uttrakhand\n"
        "🇮🇳 Country: India\n"
        "💻 Role:  Developer and coder\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "🤖 About Owner:\n"
        "This bot is created and maintained by the owner.\n\n"
        "🚀 More features will be added in the future."
    )


# =========================================================
# HELP COMMAND
# =========================================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🆘 BOT HELP & FEATURES\n\n"

        "📌 CURRENT FEATURES\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "▶️ /start - Bot start karne ke liye\n"
        "👑 /ownersprofile - Bot owner ki information\n"
        "🗑️ /erase - Apna bot data erase karne ke liye\n"
        "❓ /help - Bot ke features dekhne ke liye\n"
        "📚 /resources - Resources lene ke liye\n\n"

        "🔑 SPECIAL KEYWORD\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "💬 Keyword: goddymonor\n"
        "Is keyword ko message mein use karne par special message milega.\n\n"

        "🚀 FUTURE USES\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "📚 Notes & PDFs\n"
        "🎥 Educational Videos\n"
        "🤖 AI Chat\n"
        "🌐 Translation\n"
        "🧠 Smart Commands\n"
        "👤 User Profiles\n"
        "🔍 Search Features\n"
        "📢 Automatic Updates\n\n"

        "💗 Bot ko time ke saath aur useful banaya jayega."
    )


# =========================================================
# ERASE COMMAND
# =========================================================

async def erase(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "✅ Confirm",
                callback_data="erase_confirm"
            ),
            InlineKeyboardButton(
                "❌ Not Confirm",
                callback_data="erase_cancel"
            )
        ]
    ]

    await update.message.reply_text(
        "⚠️ Are you sure?\n\n"
        "Aapka bot data erase kar diya jayega.\n\n"
        "Neeche option select karo 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# ERASE BUTTON HANDLER
# =========================================================

async def erase_button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == "erase_confirm":

        if user_id in user_data:
            del user_data[user_id]

        await query.edit_message_text(
            "✅ Data erased successfully.\n\n"
            "Aapka bot data delete kar diya gaya hai."
        )

    elif query.data == "erase_cancel":

        await query.edit_message_text(
            "❌ Erase cancelled.\n\n"
            "Aapka data delete nahi hua."
        )


# =========================================================
# SPECIAL KEYWORD
# =========================================================

async def special_keyword(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if "goddymonor" in text.lower():

        await update.message.reply_text(
            "💗 love you every one \n\n"
            "future mai aapko kuch chaiiye is bot mai to is bot ke owner ko msg kar lena \n"
            "this side goddex monor 😊"
        )
        return

    reply = (
        "Goddy se love karte ho to share karna 😊\n\n"
        "Aur bhi bahut saare resources yahan milenge.\n\n"
        "Hamara motive yahi rahega ki aap sabko more information mile."
    )

    await update.message.reply_text(reply)


# =========================================================
# RESOURCES COMMAND
# =========================================================

async def resources(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "❤ Love me",
                url="https://www.codewithharry.com/notes"
            )
        ]
    ]

    await update.message.reply_text(
        "🎥 Goddy pe bharosa karo, ek click karo\n\n"
        "Neeche link select karo 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# SERVER
# =========================================================

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")


def run_server():
    HTTPServer(
        ("0.0.0.0", int(os.environ.get("PORT", 10000))),
        H
    ).serve_forever()


threading.Thread(target=run_server, daemon=True).start()


# =========================================================
# START COMMAND
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    name = update.effective_user.first_name

    text = f"""<b>⚡️ SYSTEM ONLINE ⚡️</b>

<pre>
┌──[ GODDEX_ERA@terminal ]
│
├─ 🔓 Access Granted
├─ 👤 User  : {name}
├─ 👑 Owner : Goddex
├─ 📡 Channel : Goddex Era
└─ 🟢 Status : Connected
</pre>

<b>💀 Welcome to the matrix, {name}.</b>

<code>$ initializing bot...  [██████████] 100%</code>

🚀 Tap below to continue
🔥 <i>Powered by Goddex Era</i> 🔥"""

    keyboard = [
        [InlineKeyboardButton("📡 Join Channel", url="https://t.me/goddyschannel")],
        [InlineKeyboardButton("👑 Contact Owner", url="t.me/Imgodex")],
    ]

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# =========================================================
# BUTTON HANDLER
# =========================================================

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


# =========================================================
# BOT SETUP
# =========================================================

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(CommandHandler("ownersprofile", ownersprofile))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("erase", erase))
app.add_handler(CommandHandler("resources", resources))

app.add_handler(CallbackQueryHandler(erase_button, pattern="^erase_"))
app.add_handler(CallbackQueryHandler(button))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        special_keyword
    )
)

print("Bot chal gaya!")
app.run_polling()
