import telebot
import yt_dlp
import os
from telebot import types

# التوكن الخاص بك (يرجى تغييره للأمان)
TOKEN = '8235603726:AAHA14coek5rb90rLwO80vkDAMKaId2bw0g'
bot = telebot.TeleBot(TOKEN)

AD_LINK = "https://www.effectivegatecpm.com/xaeg3i863?key=23cf5c1f0aa47c762d8b1fc9de714230"
CHANNEL_USER = "@husam22227"

# قاموس لتتبع عدد التحميلات
user_downloads = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🎬 أرسل رابط تيك توك للتحميل بجودة عالية!")

@bot.callback_query_handler(func=lambda call: call.data == "reset_counter")
def reset_counter(call):
    user_id = call.from_user.id
    # تصفير العداد للمستخدم
    user_downloads[user_id] = 0
    
    # تحديث الرسالة لتأكيد التصفير
    bot.answer_callback_query(call.id, "✅ تم تصفير العداد بنجاح!")
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="🔓 تم فتح التحميل من جديد! يمكنك الآن إرسال 3 روابط أخرى."
    )

@bot.message_handler(func=lambda message: True)
def handle_download(message):
    user_id = message.from_user.id
    url = message.text

    # التحقق من العداد
    current_count = user_downloads.get(user_id, 0)
    
    if current_count >= 3:
        markup = types.InlineKeyboardMarkup()
        # زر الرابط
        btn_link = types.InlineKeyboardButton("🔗 اضغط لفتح الرابط", url=AD_LINK)
        # زر التصفير (تأكد أن الـ callback_data مطابق تماماً للمعالج فوق)
        btn_done = types.InlineKeyboardButton("✅ تم الفتح، أعد التصفير", callback_data="reset_counter")
        
        markup.add(btn_link)
        markup.add(btn_done)
        
        bot.reply_to(message, "⚠️ توقف! لقد وصلت للحد الأقصى (3 فيديوهات).\n\nيجب فتح الرابط أولاً ثم الضغط على زر التصفير لتتمكن من التحميل مجدداً.", reply_markup=markup)
        return

    if "tiktok.com" not in url:
        bot.reply_to(message, "❌ نعتذر، الرابط يجب أن يكون من تيك توك.")
        return

    msg = bot.reply_to(message, "⏳ جاري المعالجة...")
    
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'vid_{user_id}.%(ext)s',
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video, caption=f"✅ تم التحميل ({current_count + 1}/3)")
        
        # زيادة العداد بعد نجاح الإرسال
        user_downloads[user_id] = current_count + 1
        
        if os.path.exists(filename): os.remove(filename)
        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ حدث خطأ غير متوقع.", message.chat.id, msg.message_id)

bot.infinity_polling()
