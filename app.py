import telebot
import yt_dlp
import os
from telebot import types

# التوكن الخاص بك
TOKEN = '8235603726:AAHA14coek5rb90rLwO80vkDAMKaId2bw0g'
bot = telebot.TeleBot(TOKEN)

AD_LINK = "https://www.effectivegatecpm.com/xaeg3i863?key=23cf5c1f0aa47c762d8b1fc9de714230"
CHANNEL_USER = "@husam22227"

# --- 1. معالج الأزرار (يجب أن يكون في البداية) ---
@bot.callback_query_handler(func=lambda call: call.data == "get_vid")
def send_the_video(call):
    user_id = call.from_user.id
    filename = f"video_{user_id}.mp4"

    if os.path.exists(filename):
        bot.answer_callback_query(call.id, "🚀 جاري إرسال الفيديو... انتظر قليلاً")
        try:
            with open(filename, 'rb') as video:
                bot.send_video(call.message.chat.id, video, caption=f"✅ تم التحميل بنجاح!\n📢 تابعنا: {CHANNEL_USER}")
            
            # حذف الملف بعد الإرسال الناجح
            os.remove(filename)
            # حذف رسالة الأزرار لتنظيف المحادثة
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception as e:
            bot.answer_callback_query(call.id, "❌ خطأ أثناء الإرسال.", show_alert=True)
    else:
        # إذا ضغط المستخدم مرتين أو الملف غير موجود
        bot.answer_callback_query(call.id, "⚠️ الملف غير موجود أو تم إرساله مسبقاً. أرسل الرابط من جديد.", show_alert=True)

# --- 2. معالج الأوامر ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🎬 أهلاً بك! أرسل رابط تيك توك الآن وسأقوم بتجهيزه لك.")

# --- 3. معالج الروابط والتحميل ---
@bot.message_handler(func=lambda message: True)
def handle_download(message):
    url = message.text
    user_id = message.from_user.id
    
    if "tiktok.com" not in url:
        bot.reply_to(message, "❌ نعتذر، الرابط يجب أن يكون من تيك توك فقط.")
        return

    # حذف أي ملف قديم لهذا المستخدم لضمان عدم حدوث تداخل
    old_file = f"video_{user_id}.mp4"
    if os.path.exists(old_file): os.remove(old_file)

    msg = bot.reply_to(message, "⏳ جاري تحميل الفيديو على سيرفراتنا...")

    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': old_file,
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            thumb = info.get('thumbnail', None)

        # إنشاء الأزرار
        markup = types.InlineKeyboardMarkup()
        btn_ad = types.InlineKeyboardButton("🔓 تفعيل سيرفر التحميل (إعلان)", url=AD_LINK)
        btn_send = types.InlineKeyboardButton("📥 استلام الفيديو الآن", callback_data="get_vid")
        markup.add(btn_ad)
        markup.add(btn_send)

        # إرسال النتيجة للمستخدم
        if thumb:
            bot.send_photo(message.chat.id, thumb, 
                         caption="✅ الفيديو جاهز الآن!\n\n1️⃣ اضغط على 'تفعيل السيرفر' أولاً.\n2️⃣ ثم اضغط على 'استلام الفيديو' بالأسفل.", 
                         reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "✅ الفيديو جاهز! اضغط على الأزرار أدناه للاستلام:", reply_markup=markup)
        
        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ حدث خطأ أثناء التجهيز. تأكد من أن الفيديو ليس خاصاً.", message.chat.id, msg.message_id)

bot.infinity_polling()
