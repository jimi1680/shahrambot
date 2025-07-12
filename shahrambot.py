import os
import openai
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# تنظیم لاگر برای چاپ خطاها در Render
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# خواندن کلیدها از متغیرهای محیطی
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

# بررسی وجود کلیدها
if TELEGRAM_TOKEN is None:
    raise ValueError("❌ متغیر BOT_TOKEN تنظیم نشده!")

if OPENAI_KEY is None:
    raise ValueError("❌ متغیر OPENAI_KEY تنظیم نشده!")

openai.api_key = OPENAI_KEY

# تابع دریافت پاسخ از ChatGPT
async def ask_gpt(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}]
    )
    return response.choices[0].message.content.strip()

# ساخت کیبورد سفارشی
keyboard = [
    [KeyboardButton("سلام 👋"), KeyboardButton("درباره ما ℹ️")],
    [KeyboardButton("جوک بگو 😂"), KeyboardButton("توصیه مطالعه 📚")]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# هندلر دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! من ربات متصل به ChatGPT هستم. هر چی دوست داری بپرس 🤖",
        reply_markup=reply_markup
    )

# هندلر پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.chat.send_action(action="typing")
    try:
        reply = await ask_gpt(user_message)
        await update.message.reply_text(reply)
    except Exception as e:
        logging.error(f"❌ خطا در پاسخ‌دهی ChatGPT: {e}")
        await update.message.reply_text("❌ خطا در پاسخ‌دهی:\n" + str(e))

# اجرای برنامه
if __name__ == "__main__":
    try:
        app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        logging.info("✅ ربات با موفقیت اجرا شد.")
        app.run_polling()
    except Exception as e:
        logging.error(f"❌ خطا در اجرای ربات: {e}")
