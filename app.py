import telebot
import yt_dlp
import os
from telebot import types

# التوكن الخاص بك
TOKEN = '8235603726:AAHA14coek5rb90rLwO80vkDAMKaId2bw0g'
bot = telebot.TeleBot(TOKEN)

AD_LINK = "https://www.effectivegatecpm.com/xaeg3i863?key=23cf5c1f0aa47c762d8b1fc9de714230"
CHANNEL_USER = "@husam22227"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🎬 أهلاً بك! أرسل رابط تيك توك الآن لتجهيزه.")

@bot.message_handler(func=lambda message: "tiktok.com" in message.text)
def prepare_video(message):
    url = message.text
    user_id = message.from_user.id
    msg = bot.reply_to(message, "⏳ جاري تجهيز الفيديو... انتظر قليلاً")

    # اسم ملف ثابت لكل مستخدم لتجنب مشاكل الـ Callback Data
    filename = f"video_{user_id}.mp4"

    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': filename,
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            thumb = info.get('thumbnail', None)

        # إنشاء الأزرار
        markup = types.InlineKeyboardMarkup()
        btn_ad = types.InlineKeyboardButton("🔓 تفعيل سيرفر التحميل (مهم)", url=AD_LINK)
        # نرسل 'get_vid' فقط في الـ callback_data
        btn_send = types.InlineKeyboardButton("📥 استلام الفيديو الآن", callback_data="get_vid")
        markup.add(btn_ad)
        markup.add(btn_send)

        if thumb:
            bot.send_photo(message.chat.id, thumb, caption="✅ الفيديو أصبح جاهزاً!\n\nاضغط على 'تفعيل السيرفر' أولاً ثم اضغط استلام.", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "✅ الفيديو جاهز! اضغط على الأزرار أدناه:", reply_markup=markup)
        
        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ حدث خطأ: {e}", message.chat.id, msg.message_id)

# هذا هو المعالج الذي يصلح مشكلة الزر
@bot.callback_query_handler(func=lambda call: call.data == "get_vid")
def send_the_video(call):
    user_id = call.from_user.id
    filename = f"video_{user_id}.mp4"

    if os.path.exists(filename):
        bot.answer_callback_query(call.id, "🚀 جاري إرسال الفيديو...")
        with open(filename, 'rb') as video:
            bot.send_video(call.message.chat.id, video, caption=f"✅ تم التحميل بنجاح!\n📢 {CHANNEL_USER}")
        
        # حذف الملف بعد الإرسال
        os.remove(filename)
        # حذف رسالة الأزرار
        bot.delete_message(call.message.chat.id, call.message.message_id)
    else:
        # إذا لم يجد الملف (ربما تم حذفه أو لم يكتمل التحميل)
        bot.answer_callback_query(call.id, "⚠️ الملف غير موجود، أرسل الرابط مرة أخرى.", show_alert=True)

bot.infinity_polling()
