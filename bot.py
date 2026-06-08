from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8874734813:AAHHd8MTlhJSHPsmjQDBNChQs215JvEVpN0"

ADMIN_ID = 8559323592
WALLET = "TFcLisJ8jTNTBbTU2LoGC3Mo6AQ1UnzJw5"

PRIVATE_CHANNEL_LINK = "https://t.me/+m5tt78scF2RhODFk"
PRIVATE_CHANNEL_LINK2 = "https://t.me/+MHIdsX4IcysyODVk"

PUBLIC_CHANNEL = "https://t.me/Dr_6_Khaled"
SUPPORT = "@Dr_7_Khaled"


def main_menu():
    keyboard = [
        [InlineKeyboardButton("📊 مميزات القناة", callback_data="features")],
        [InlineKeyboardButton("💎 أسعار الاشتراك", callback_data="prices")],
        [InlineKeyboardButton("💳 الدفع", callback_data="payment")],
        [InlineKeyboardButton("📈 نتائج التوصيات", callback_data="results")],
        [InlineKeyboardButton("🔐 الاشتراك بالقناة الخاصة", callback_data="subscribe")],
        [InlineKeyboardButton("📞 التواصل", callback_data="support")],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً بك في بوت Dr Khaled\n\nاختر من القائمة:",
        reply_markup=main_menu()
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "features":
        text = """📊 مميزات القناة الخاصة

✅ توصيات يومية فيوتشر وسبوت
✅ من 3 إلى 6 توصيات فيوتشر يومياً
✅ من 3 إلى 6 توصيات سبوت يومياً
✅ أرباح الفيوتشر اليومية من 50% إلى 500%
✅ أرباح السبوت اليومية من 5% إلى 50%
✅ نسبة نجاح التوصيات 85%
"""
        await query.message.reply_text(text, reply_markup=main_menu())

    elif query.data == "prices":
        text = """💎 أسعار الاشتراك في القناة الخاصة ✅

🔹 اشتراك شهر = 30$
🔹 اشتراك شهرين = 60$
🔹 اشتراك 3 أشهر = 80$
🔹 اشتراك سنة كاملة = 200$
"""
        await query.message.reply_text(text, reply_markup=main_menu())

    elif query.data == "payment":
        text = f"""💳 الدفع عبر USDT TRC20

عنوان المحفظة:

{WALLET}

📸 بعد التحويل أرسل صورة إثبات الدفع هنا.
"""
        await query.message.reply_text(text, reply_markup=main_menu())

    elif query.data == "results":
        await query.message.reply_text(
            f"📈 نتائج التوصيات:\n{PUBLIC_CHANNEL}",
            reply_markup=main_menu()
        )

    elif query.data == "subscribe":
        await query.message.reply_text(
            "🔐 للاشتراك بالقناة الخاصة:\n\n1️⃣ ادفع على المحفظة\n2️⃣ أرسل صورة التحويل هنا\n3️⃣ بعد الموافقة تصلك روابط القناتين الخاصة",
            reply_markup=main_menu()
        )

    elif query.data == "support":
        await query.message.reply_text(
            f"📞 حساب الدعم الفني:\n{SUPPORT}",
            reply_markup=main_menu()
        )


async def receive_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    photo = update.message.photo[-1]

    keyboard = [[
        InlineKeyboardButton("✅ قبول الاشتراك", callback_data=f"approve_{user.id}"),
        InlineKeyboardButton("❌ رفض الاشتراك", callback_data=f"reject_{user.id}")
    ]]

    caption = f"""📥 إثبات تحويل جديد

👤 الاسم: {user.full_name}
🔗 اليوزر: @{user.username}
🆔 ID: {user.id}
"""

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo.file_id,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    await update.message.reply_text(
        "✅ تم استلام إثبات الدفع.\nسيتم مراجعة الطلب وتفعيل الاشتراك قريباً."
    )


async def admin_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id != ADMIN_ID:
        await query.message.reply_text("❌ هذا الزر للمدير فقط")
        return

    data = query.data

    if data.startswith("approve_"):
        user_id = int(data.replace("approve_", ""))

        await context.bot.send_message(
            chat_id=user_id,
            text=f"""✅ تم تفعيل اشتراكك بنجاح.

🔐 رابط القناة الأولى:
{PRIVATE_CHANNEL_LINK}

🔐 رابط القناة الثانية:
{PRIVATE_CHANNEL_LINK2}
"""
        )

        await query.message.reply_text("✅ تم قبول الاشتراك.")

    elif data.startswith("reject_"):
        user_id = int(data.replace("reject_", ""))

        await context.bot.send_message(
            chat_id=user_id,
            text="❌ تم رفض طلب الاشتراك.\nيرجى التواصل مع الدعم."
        )

        await query.message.reply_text("❌ تم رفض الطلب.")


async def receive_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📸 إذا دفعت، أرسل صورة التحويل هنا.")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(admin_buttons, pattern="^(approve_|reject_)"))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.PHOTO, receive_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_text))

    print("Bot Started...")
    app.run_polling()


if __name__ == "__main__":
    main()
