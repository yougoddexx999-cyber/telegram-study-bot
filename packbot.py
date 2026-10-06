import os
import sqlite3
import json
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

from openai import OpenAI


# =========================================================
# API KEYS
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


# =========================================================
# DUMMY USER DATA
# =========================================================

user_data = {}


# =========================================================
# DATABASE
# =========================================================

db = sqlite3.connect("bot_memory.db", check_same_thread=False)
cursor = db.cursor()


# ---------------------------------------------------------
# USERS TABLE
# ---------------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    gender TEXT,
    mode TEXT
)
""")


# ---------------------------------------------------------
# CHAT MEMORY TABLE
# ---------------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    role TEXT,
    message TEXT
)
""")


# ---------------------------------------------------------
# SMART MEMORY TABLE
# ---------------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS smart_memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    memory_key TEXT,
    memory_value TEXT
)
""")

db.commit()


# =========================================================
# USER SETTINGS FUNCTIONS
# =========================================================

def save_user(user_id, gender=None, mode=None):

    cursor.execute(
        "SELECT user_id FROM users WHERE user_id = ?",
        (user_id,)
    )

    existing_user = cursor.fetchone()

    if existing_user:

        if gender is not None:
            cursor.execute(
                """
                UPDATE users
                SET gender = ?
                WHERE user_id = ?
                """,
                (gender, user_id)
            )

        if mode is not None:
            cursor.execute(
                """
                UPDATE users
                SET mode = ?
                WHERE user_id = ?
                """,
                (mode, user_id)
            )

    else:

        cursor.execute(
            """
            INSERT INTO users
            (user_id, gender, mode)
            VALUES (?, ?, ?)
            """,
            (
                user_id,
                gender,
                mode
            )
        )

    db.commit()


def get_user_settings(user_id):

    cursor.execute(
        """
        SELECT gender, mode
        FROM users
        WHERE user_id = ?
        """,
        (user_id,)
    )

    result = cursor.fetchone()

    if result:

        return {
            "gender": result[0],
            "mode": result[1] or "friendly"
        }

    return {
        "gender": None,
        "mode": "friendly"
    }


# =========================================================
# CHAT MEMORY FUNCTIONS
# =========================================================

def save_message(user_id, role, message):

    cursor.execute(
        """
        INSERT INTO chat_memory
        (user_id, role, message)
        VALUES (?, ?, ?)
        """,
        (
            user_id,
            role,
            message
        )
    )

    db.commit()


def get_chat_memory(user_id, limit=20):

    cursor.execute(
        """
        SELECT role, message
        FROM chat_memory
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (
            user_id,
            limit
        )
    )

    messages = cursor.fetchall()

    messages.reverse()

    return messages


# =========================================================
# SMART MEMORY FUNCTIONS
# =========================================================

def save_smart_memory(user_id, key, value):

    if not value:
        return

    value = str(value).strip()

    if not value:
        return

    cursor.execute(
        """
        SELECT id
        FROM smart_memory
        WHERE user_id = ?
        AND memory_key = ?
        """,
        (
            user_id,
            key
        )
    )

    existing = cursor.fetchone()

    if existing:

        cursor.execute(
            """
            UPDATE smart_memory
            SET memory_value = ?
            WHERE user_id = ?
            AND memory_key = ?
            """,
            (
                value,
                user_id,
                key
            )
        )

    else:

        cursor.execute(
            """
            INSERT INTO smart_memory
            (user_id, memory_key, memory_value)
            VALUES (?, ?, ?)
            """,
            (
                user_id,
                key,
                value
            )
        )

    db.commit()


def get_smart_memory(user_id):

    cursor.execute(
        """
        SELECT memory_key, memory_value
        FROM smart_memory
        WHERE user_id = ?
        """,
        (user_id,)
    )

    return cursor.fetchall()


# =========================================================
# SMART MEMORY EXTRACTION
# =========================================================

def extract_smart_memory(user_id, text):

    try:

        prompt = f"""
You are a memory extraction system.

Analyze the user's message below.

Only identify information that is useful for future conversations.

Possible categories:

name
interest
goal
preference
study_topic
language

Do NOT save:
- passwords
- API keys
- phone numbers
- email addresses
- exact addresses
- highly sensitive personal information
- temporary/random statements

Return ONLY valid JSON.

Example:

{{
    "name": "Rahul",
    "interest": "C programming",
    "goal": "learn Python"
}}

If nothing important is present, return:

{{}}

User message:

{text}
"""

        response = client.responses.create(
            model="gpt-5-mini",
            instructions=prompt,
            input=text
        )

        result = response.output_text.strip()

        # Remove markdown JSON fences if model adds them
        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

        memories = json.loads(result)

        if isinstance(memories, dict):

            for key, value in memories.items():

                if value:

                    save_smart_memory(
                        user_id,
                        key,
                        value
                    )

    except Exception as e:

        print("MEMORY ERROR:", e)


# =========================================================
# OWNER PROFILE
# =========================================================

async def ownersprofile(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👑 OWNER PROFILE\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "👤 Name: goddex\n"
        "📧 Email: yougoddexx@gmail.com\n"
        "📱 Phone: +91 xxxxxxxxxx\n"
        "🎂 Age: 19\n"
        "🎓 College: almora diploma college\n"
        "📍 State: uttrakhand\n"
        "🇮🇳 Country: India\n"
        "💻 Role: Developer and coder\n"
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
        "📚 /resources - Resources lene ke liye\n"
        "⚙️ /settings - AI settings change karne ke liye\n\n"

        "🤖 AI FEATURES\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "💬 AI Chat\n"
        "🧠 Conversation Memory\n"
        "⭐ Smart Memory\n"
        "👤 Gender Preference\n"
        "🧑‍🤝‍🧑 Friendly Mode\n"
        "👨‍🏫 Teacher Mode\n"
        "🌐 Hindi / English / Hinglish\n\n"

        "🔑 SPECIAL KEYWORD\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "💬 Keyword: goddymonor\n\n"

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
        "Isme settings aur AI memory bhi delete hogi.\n\n"
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

        # Old temporary data
        if user_id in user_data:
            del user_data[user_id]

        # User settings
        cursor.execute(
            "DELETE FROM users WHERE user_id = ?",
            (user_id,)
        )

        # Chat memory
        cursor.execute(
            "DELETE FROM chat_memory WHERE user_id = ?",
            (user_id,)
        )

        # Smart memory
        cursor.execute(
            "DELETE FROM smart_memory WHERE user_id = ?",
            (user_id,)
        )

        db.commit()

        await query.edit_message_text(
            "✅ Data erased successfully.\n\n"
            "🧠 AI memory deleted.\n"
            "⚙️ Settings deleted.\n"
            "💬 Chat history deleted."
        )

    elif query.data == "erase_cancel":

        await query.edit_message_text(
            "❌ Erase cancelled.\n\n"
            "Aapka data delete nahi hua."
        )


# =========================================================
# SPECIAL KEYWORD + AI CHAT
# =========================================================

async def special_keyword(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    user_id = update.effective_user.id

    # -----------------------------------------------------
    # SPECIAL KEYWORD
    # -----------------------------------------------------

    if "goddymonor" in text.lower():

        await update.message.reply_text(
            "💗 love you every one \n\n"
            "future mai aapko kuch chaiiye is bot mai to is bot ke owner ko msg kar lena \n"
            "this side goddex monor 😊"
        )

        return

    try:

        # -------------------------------------------------
        # GET SETTINGS
        # -------------------------------------------------

        settings = get_user_settings(user_id)

        gender = settings["gender"]
        mode = settings["mode"]

        # -------------------------------------------------
        # GET SMART MEMORY
        # -------------------------------------------------

        smart_memories = get_smart_memory(user_id)

        memory_text = ""

        if smart_memories:

            memory_text = "\n".join(
                f"{key}: {value}"
                for key, value in smart_memories
            )

        else:

            memory_text = "No important memories stored yet."

        # -------------------------------------------------
        # GET RECENT CHAT
        # -------------------------------------------------

        previous_messages = get_chat_memory(
            user_id,
            limit=20
        )

        conversation = []

        for role, message in previous_messages:

            conversation.append(
                {
                    "role": role,
                    "content": message
                }
            )

        # -------------------------------------------------
        # PERSONALITY
        # -------------------------------------------------

        if mode == "friendly":

            instructions = f"""
You are a friendly AI chatbot.

Talk naturally like a close, supportive friend.

Use Hinglish when the user uses Hinglish.
Use Hindi when the user uses Hindi.
Use English when the user uses English.

The user's gender preference is:
{gender or "not selected"}

Do not stereotype the user based on gender.

Understand the user's mood from their message.

If the user is:
- happy → suitable happy emojis can be used
- sad → supportive emojis such as ❤️ 🫂 can be used
- confused → suitable emojis such as 🤔 💡 can be used
- studying → suitable emojis such as 📚 🧠 💻 can be used
- joking → suitable funny emojis can be used

Do not spam emojis.
Use emojis naturally.

Be emotionally supportive when appropriate.

Never pretend to be a real human.
You are an AI assistant.

IMPORTANT USER MEMORY:
{memory_text}
"""

        else:

            instructions = f"""
You are a helpful AI teacher.

Explain things clearly and step by step.

Use simple language.

Use Hinglish when the user uses Hinglish.
Use Hindi when the user uses Hindi.
Use English when the user uses English.

The user's gender preference is:
{gender or "not selected"}

Do not stereotype the user based on gender.

Keep the response educational, structured and easy to understand.

Avoid unnecessary emojis.

You are an AI assistant, not a real human.

IMPORTANT USER MEMORY:
{memory_text}
"""

        # -------------------------------------------------
        # ADD CURRENT USER MESSAGE
        # -------------------------------------------------

        conversation.append(
            {
                "role": "user",
                "content": text
            }
        )

        # -------------------------------------------------
        # MAIN AI RESPONSE
        # -------------------------------------------------

        response = client.responses.create(
            model="gpt-5-mini",
            instructions=instructions,
            input=conversation
        )

        reply = response.output_text.strip()

        # -------------------------------------------------
        # SAVE USER MESSAGE
        # -------------------------------------------------

        save_message(
            user_id,
            "user",
            text
        )

        # -------------------------------------------------
        # SAVE AI MESSAGE
        # -------------------------------------------------

        save_message(
            user_id,
            "assistant",
            reply
        )

        # -------------------------------------------------
        # SMART MEMORY
        # -------------------------------------------------

        extract_smart_memory(
            user_id,
            text
        )

        # -------------------------------------------------
        # SEND RESPONSE
        # -------------------------------------------------

    

    except Exception as e:
        
        print("AI ERROR:", e)

        await update.message.reply_text(
        f"AI Error: {e}"
    )

# =========================================================
# SETTINGS COMMAND
# =========================================================

async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    settings = get_user_settings(user_id)

    gender = settings["gender"] or "Not selected"
    mode = settings["mode"] or "friendly"

    keyboard = [
        [
            InlineKeyboardButton(
                "👤 Gender",
                callback_data="settings_gender"
            ),
            InlineKeyboardButton(
                "💬 Mode",
                callback_data="settings_mode"
            )
        ]
    ]

    await update.message.reply_text(
        "⚙️ BOT SETTINGS\n\n"
        f"👤 Gender: {gender}\n"
        f"💬 Mode: {mode}\n\n"
        "Neeche se setting change karo 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# SETTINGS BUTTON HANDLER
# =========================================================

async def settings_button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "settings_gender":

        keyboard = [
            [
                InlineKeyboardButton(
                    "♂️ Male",
                    callback_data="gender_male"
                ),
                InlineKeyboardButton(
                    "♀️ Female",
                    callback_data="gender_female"
                )
            ]
        ]

        await query.edit_message_text(
            "👤 Select your gender preference 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "settings_mode":

        keyboard = [
            [
                InlineKeyboardButton(
                    "🧑‍🤝‍🧑 Friendly",
                    callback_data="mode_friendly"
                ),
                InlineKeyboardButton(
                    "👨‍🏫 Teacher",
                    callback_data="mode_teacher"
                )
            ]
        ]

        await query.edit_message_text(
            "💬 Select conversation mode 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# =========================================================
# GENDER BUTTON
# =========================================================

async def gender_button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == "gender_male":

        save_user(
            user_id,
            gender="male"
        )

        await query.edit_message_text(
            "♂️ Male preference selected.\n\n"
            "AI settings update ho gayi hain."
        )

    elif query.data == "gender_female":

        save_user(
            user_id,
            gender="female"
        )

        await query.edit_message_text(
            "♀️ Female preference selected.\n\n"
            "AI settings update ho gayi hain."
        )


# =========================================================
# MODE BUTTON
# =========================================================

async def mode_button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == "mode_friendly":

        save_user(
            user_id,
            mode="friendly"
        )

        await query.edit_message_text(
            "🧑‍🤝‍🧑 Friendly Mode ON!\n\n"
            "Ab AI friendly aur casual style mein baat karega 😄"
        )

    elif query.data == "mode_teacher":

        save_user(
            user_id,
            mode="teacher"
        )

        await query.edit_message_text(
            "👨‍🏫 Teacher Mode ON!\n\n"
            "Ab AI clear aur step-by-step style mein explain karega."
        )


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
        (
            "0.0.0.0",
            int(os.environ.get("PORT", 10000))
        ),
        H
    ).serve_forever()


threading.Thread(
    target=run_server,
    daemon=True
).start()


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
        [
            InlineKeyboardButton(
                "📡 Join Channel",
                url="https://t.me/goddyschannel"
            )
        ],
        [
            InlineKeyboardButton(
                "👑 Contact Owner",
                url="t.me/Imgodex"
            )
        ],
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


# ---------------------------------------------------------
# COMMANDS
# ---------------------------------------------------------

app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    CommandHandler("ownersprofile", ownersprofile)
)

app.add_handler(
    CommandHandler("help", help_command)
)

app.add_handler(
    CommandHandler("erase", erase)
)

app.add_handler(
    CommandHandler("resources", resources)
)

app.add_handler(
    CommandHandler("settings", settings_command)
)


# ---------------------------------------------------------
# CALLBACK BUTTONS
# ---------------------------------------------------------

app.add_handler(
    CallbackQueryHandler(
        erase_button,
        pattern="^erase_"
    )
)

app.add_handler(
    CallbackQueryHandler(
        settings_button,
        pattern="^settings_"
    )
)

app.add_handler(
    CallbackQueryHandler(
        gender_button,
        pattern="^gender_"
    )
)

app.add_handler(
    CallbackQueryHandler(
        mode_button,
        pattern="^mode_"
    )
)

app.add_handler(
    CallbackQueryHandler(button)
)


# ---------------------------------------------------------
# NORMAL TEXT → AI
# ---------------------------------------------------------

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        special_keyword
    )
)


# =========================================================
# START BOT
# =========================================================

print("Bot chal gaya!")

app.run_polling()
