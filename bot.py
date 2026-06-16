from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import openai

TOKEN = "8874734813:AAHHd8MTlhJSHPsmjQDBNChQs215JvEVpN0"
OPENROUTER_API_KEY = "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"

openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = OPENROUTER_API_KEY

ADMIN_ID = 8559323592
USDT_ADDRESS = "TQ5bf2cVuBaTNmE8woNdyDsoAWQJdwMaef"
NETWORK = "TRC20"
CONTACT = "@Dr_7_Khaled"
RESULTS_CHANNEL = "https://t.me/Dr_6_Khaled"

PRIVATE_CHANNELS = """
✅ تم قبول اشتراكك

روابط القنوات الخاصة:

القناة الأولى:
https://t.me/+eRhZxFFl0oYwN2Zk

القناة الثانية:
https://t.me/+D7do_Sb7MoxjYmZk
"""

keyboard = [
    ["💎 أسعار الاشتراك", "🎥 شرح التحويل"],
    ["📊 ميزات القناة", "💳 الدفع"],
    ["📈 نتائج التوصيات", "📢 قناة النتائج"],
    ["🔐 الاشتراك بالقناة", "📞 التواصل"],
    ["❓ الأسئلة الشائعة"]
]

markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def ai_answer(user_text):
    try:
        res = openai.ChatCompletion.create(
            model="openai/gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"""
أنت Dr Khaled، موظف مبيعات حقيقي لقناة توصيات كريبتو.

تكلم عربي طبيعي وقصير كأنك شخص في تيليجرام.
لا تكرر الترحيب.
لا تكرر الأسعار إلا إذا طلبها العميل.
لا تقل لا نقدم فيوتشر أو سبوت.
إذا سأل عن فيوتشر أو سبوت قل: عندنا توصيات فيوتشر وسبوت يومياً.
إذا قال مهتم أو نعم اسأله: أي باقة تناسبك؟
إذا اعترض أو قال نصاب رد بهدوء وثقة ووجهه لقناة النتائج.
إذا سأل عن النتائج أرسل: {RESULTS_CHANNEL}
إذا سأل عن التواصل أرسل: {CONTACT}
إذا قال دفعت أو حولت اطلب صورة الإيصال.

الأسعار:
شهر 30 دولار
شهرين 60 دولار
3 أشهر 80 دولار
سنة 200 دولار

إذا اختار العميل باقة ووافق، لا تكتب كلمة العنوان. اكتب عنوان المحفظة فقط في سطر مستقل، ثم اكتب: الشبكة TRC20 في السطر التالي.
{USDT_ADDRESS}
الشبكة TRC20

هدفك تقنع العميل بالاشتراك بدون إطالة.
"""
                },
                {"role": "user", "content": user_text}
            ],
            max_tokens=180,
            temperature=0.9
        )
        return res["choices"][0]["message"]["content"]
    except Exception as e:
        return "حدث خطأ مؤقت، جرّب مرة ثانية."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً وسهلاً فيك 👋\nأنا مساعدك الخاص بالقناة.\nاكتب سؤالك أو اختر من الأزرار بالأسفل.",
        reply_markup=markup
    )

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text == "💎 أسعار الاشتراك":
        await update.message.reply_text("💎 الأسعار:\n\nشهر: 30$\nشهرين: 60$\n3 أشهر: 80$\nسنوي: 200$")

    elif text == "📊 ميزات القناة":
        await update.message.reply_text(
            "📊 مميزات القناة:\n\n"
            "✅ توصيات يومية فيوتشر وسبوت\n"
            "✅ من 3 إلى 6 توصيات فيوتشر يومياً\n"
            "✅ من 3 إلى 6 توصيات سبوت يومياً\n"
            "✅ نسبة نجاح التوصيات 85%\n"
            "🔥 متابعة مستمرة للسوق"
        )

    elif text == "💳 الدفع":
        await update.message.reply_text(
            f"💳 الدفع عبر USDT\n\nالشبكة: {NETWORK}\n\nالعنوان:\n{USDT_ADDRESS}\n\n📌 هذا العنوان الي تحوله له"
        )

    elif text == "🎥 شرح التحويل":
        await update.message.reply_text(
            f"🎥 شرح التحويل:\n\n"
            f"1️⃣ افتح Binance\n"
            f"2️⃣ اختر إرسال / سحب\n"
            f"3️⃣ اختر USDT\n"
            f"4️⃣ الصق العنوان:\n{USDT_ADDRESS}\n"
            f"5️⃣ الشبكة: {NETWORK}\n"
            f"6️⃣ بعد التحويل أرسل صورة الإيصال هنا"
        )

    elif text == "📈 نتائج التوصيات":
        await update.message.reply_text(f"📈 نتائج التوصيات:\n{RESULTS_CHANNEL}")

    elif text == "📢 قناة النتائج":
        await update.message.reply_text(f"📢 قناة النتائج:\n{RESULTS_CHANNEL}")

    elif text == "🔐 الاشتراك بالقناة":
        await update.message.reply_text(
            "🔐 طريقة الاشتراك:\n\n"
            "1️⃣ اختر مدة الاشتراك\n"
            "2️⃣ حوّل USDT على شبكة TRC20\n"
            "3️⃣ أرسل صورة الإيصال هنا\n"
            "4️⃣ الإدارة تراجع الطلب\n"
            "5️⃣ بعد القبول تصلك روابط القنوات تلقائياً"
        )

    elif text == "📞 التواصل":
        await update.message.reply_text(f"📞 الحساب الرسمي:\n{CONTACT}")

    elif text == "❓ الأسئلة الشائعة":
        await update.message.reply_text(
            "❓ الأسئلة الشائعة:\n\n"
            "كيف أشترك؟ أرسل التحويل ثم صورة الإيصال.\n"
            "ما الشبكة؟ TRC20\n"
            "متى تصل الروابط؟ بعد قبول الإدارة.\n"
            f"التواصل: {CONTACT}"
        )

    else:
        user_id = update.message.from_user.id
        old = context.user_data.get("last_ai", "")
        full_text = f"الرسالة السابقة: {old}\nرسالة العميل الآن: {text}"
        answer = ai_answer(full_text)
        context.user_data["last_ai"] = f"العميل قال: {text}\nأنت رددت: {answer}"
        await update.message.reply_text(answer, reply_markup=markup)

async def receive_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    username = f"@{user.username}" if user.username else "لا يوجد"

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ قبول", callback_data=f"approve:{user_id}"),
            InlineKeyboardButton("❌ رفض", callback_data=f"reject:{user_id}")
        ]
    ])

    caption = f"📩 إيصال جديد\n\nالاسم: {user.full_name}\nاليوزر: {username}\nID: {user_id}\n\nاختر قبول أو رفض:"

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=update.message.photo[-1].file_id,
        caption=caption,
        reply_markup=buttons
    )

    await update.message.reply_text("✅ تم استلام الإيصال، سيتم مراجعته من الإدارة.", reply_markup=markup)

async def admin_decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id != ADMIN_ID:
        await query.answer("هذا الأمر خاص بالإدارة فقط.", show_alert=True)
        return

    action, user_id = query.data.split(":")
    user_id = int(user_id)

    if action == "approve":
        await context.bot.send_message(chat_id=user_id, text=PRIVATE_CHANNELS)
        await query.edit_message_caption(caption="✅ تم قبول الطلب وإرسال روابط القنوات.")

    elif action == "reject":
        await context.bot.send_message(chat_id=user_id, text=f"❌ تم رفض الإيصال.\nتواصل مع الإدارة: {CONTACT}")
        await query.edit_message_caption(caption="❌ تم رفض الطلب.")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, receive_receipt))
app.add_handler(CallbackQueryHandler(admin_decision))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

print("Bot is running...")
app.run_polling()
