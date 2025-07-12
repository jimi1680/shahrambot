import os
import openai
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# کلیدها
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")
openai.api_key = OPENAI_KEY

# پاسخ با ChatGPT
async def ask_gpt(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}]
    )
    return response.choices[0].message.content.strip()

# کیبورد سفارشی
keyboard = [
    [KeyboardButton("سلام 👋"), KeyboardButton("درباره ما ℹ️")],
    [KeyboardButton("جوک بگو 😂"), KeyboardButton("توصیه مطالعه 📚")]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! من ربات متصل به ChatGPT هستم. هر چی دوست داری بپرس 🤖",
        reply_markup=reply_markup
    )

# مدیریت پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.chat.send_action(action="typing")
    try:
        reply = await ask_gpt(user_message)
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("❌ خطا در پاسخ‌دهی:\n" + str(e))

# اجرای ربات
if __name__ == "main":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()