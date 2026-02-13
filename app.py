import telebot
import yt_dlp
import os
from telebot import types

TOKEN = '8235603726:AAHA14coek5rb90rLwO80vkDAMKaId2bw0g'
bot = telebot.TeleBot(TOKEN)

# رابط الإعلان الخاص بك
AD_LINK = "https://www.effectivegatecpm.com/xaeg3i863?key=23cf5c1f0aa47c762d8b1fc9de714230"
CHANNEL_USER = "@husam22227"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🎬 أرسل رابط تيك توك الآن وسأقوم بتجهيزه لك فوراً!")

@bot.message_handler(func=lambda message: True)
def prepare_video(message):
    url = message.text
    user_id = message.from_user.id

    if "tiktok.com" not in url:
        bot.reply_to(message, "❌ نعتذر، الرابط يجب أن يكون من تيك توك فقط.")
        return

    msg = bot.reply_to(message, "🔍 جاري فحص الفيديو وتجهيزه...")

    try:
        # إعدادات التحميل (نحمل الفيديو ونحتفظ به مؤقتاً)
        filename = f"vid_{user_id}.mp4"
        ydl_opts = {
            'format': 'best',
            'outtmpl': filename,
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            thumbnail = info.get('thumbnail', None) # استخراج صورة الفيديو

        # إنشاء الأزرار
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_ad = types.InlineKeyboardButton("🔓 فتح سيرفر التحميل (إعلان)", url=AD_LINK)
        # نرسل اسم الملف في الـ callback_data لنعرف أي فيديو سنرسل
        btn_send = types.InlineKeyboardButton("📥 استلام الفيديو الآن", callback_data=f"send_file:{filename}")
        
        markup.add(btn_ad, btn_send)

        # إرسال صورة الفيديو مع الأزرار بدلاً من الفيديو نفسه
        if thumbnail:
            bot.send_photo(message.chat.id, thumbnail, caption="✅ الفيديو جاهز للتحميل!\n\nيجب عليك فتح 'سيرفر التحميل' أولاً لتنشيط الرابط، ثم اضغط على الزر أدناه لاستلام الفيديو.", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "✅ الفيديو جاهز!\n\nاضغط على 'سيرفر التحميل' أولاً، ثم اضغط على زر الاستلام.", reply_markup=markup)

        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ حدث خطأ أثناء تجهيز الفيديو. تأكد من الرابط.", message.chat.id, msg.message_id)
        if os.path.exists(filename): os.remove(filename)

# معالج ضغطة زر "استلام الفيديو"
@bot.callback_query_handler(func=lambda call: call.data.startswith("send_file:"))
def send_the_video(call):
    filename = call.data.split(":")[1]
    
    if os.path.exists(filename):
        bot.answer_callback_query(call.id, "🚀 جاري إرسال الفيديو...")
        with open(filename, 'rb') as video:
            bot.send_video(call.message.chat.id, video, caption=f"🎬 تم التحميل بنجاح!\n📢 تابعنا: {CHANNEL_USER}")
        
        # حذف الملف من السيرفر بعد الإرسال
        os.remove(filename)
        # حذف رسالة الأزرار لترتيب المحادثة
        bot.delete_message(call.message.chat.id, call.message.message_id)
    else:
        bot.answer_callback_query(call.id, "❌ عذراً، انتهت صلاحية الرابط. أرسل الرابط مجدداً.", show_alert=True)

bot.infinity_polling()
