from telegram import Update
from telegram import ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler
from telegram.ext import  ContextTypes, MessageHandler, filters


#تابع شروع
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #ساختن کیبورد سفارشی
    keyboard = [
        ["درباره ی ما", "راهنما"],
        ["ارتباط باادمین"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard= True)
    #ارسال پیام خوش آمد و نمایش کیبورد
    await update.message.reply_text(f"سلام {update.effective_user.first_name} عزیز به ربات ما خوش آمدی",
                                    reply_markup= reply_markup)


#تابع پاسخ به دکمه ها
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    if user_message == "درباره ی ما":
        await update.message.reply_text("این ربات توسط شهرام درست شده و برای تست ویادگیری است")
    elif user_message == "راهنما":
        await update.message.reply_text("دکمه ها را لمس کن با پیام بفرست")
    elif user_message == "ارتباط باادمین":
        await update.message.reply_text("بعدا که پیشرفت کردم بهت میگم")
    else:
        await update.message.reply_text(f"تو گفتی {user_message}")
    


#ساخت  و اجرای ربات
app = ApplicationBuilder().token("8010227351:AAFnhqbzAKq9JCnW1OgoKWb2hhkrw-R87nc").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
print("ربات روشن است")
app.run_polling()
