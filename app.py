import telebot
import yt_dlp
import os
from telebot import types

TOKEN = '8235603726:AAHA14coek5rb90rLwO80vkDAMKaId2bw0g'
bot = telebot.TeleBot(TOKEN)

# الرابط المطلوب فتحه
AD_LINK = "https://www.effectivegatecpm.com/xaeg3i863?key=23cf5c1f0aa47c762d8b1fc9de714230"
CHANNEL_USER = "@husam22227"

# قاموس لتتبع عدد تحميلات كل مستخدم {user_id: count}
user_downloads = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "🎬 أهلاً بك! أرسل رابط تيك توك للتحميل."
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def download_tiktok(message):
    user_id = message.from_user.id
    url = message.text

    # 1. التحقق من عدد التحميلات
    count = user_downloads.get(user_id, 0)
    
    if count >= 3:
        markup = types.InlineKeyboardMarkup()
        btn_link = types.InlineKeyboardButton("🔗 إضغط هنا لفتح الرابط واستكمال التحميل", url=AD_LINK)
        btn_done = types.InlineKeyboardButton("✅ تم الفتح، أعد التصفير", callback_data="reset_counter")
        markup.add(btn_link)
        markup.add(btn_done)
        
        bot.reply_to(message, "⚠️ لقد استهلكت 3 تحميلات مجانية.\n\nيجب عليك فتح الرابط التالي لتتمكن من التحميل مرة أخرى:", reply_markup=markup)
        return

    # 2. التأكد أن الرابط تيك توك
    if "tiktok.com" not in url:
        bot.reply_to(message, "❌ أرسل رابط تيك توك فقط.")
        return

    msg = bot.reply_to(message, "⏳ جاري التحميل...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': f'vid_{user_id}_{count}.%(ext)s',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video, caption=f"✅ تم التحميل ({count+1}/3)")
        
        # 3. تحديث العداد للمستخدم
        user_downloads[user_id] = count + 1
        
        if os.path.exists(filename): os.remove(filename)
        bot.delete_message(message.chat.id, msg.message_id)

    except Exception:
        bot.edit_message_text("❌ فشل التحميل.", message.chat.id, msg.message_id)

# معالج ضغطة الزر لتصفير العداد
@bot.callback_query_handler(func=lambda call: call.data == "reset_counter")
def reset_counter(call):
    user_id = call.from_user.id
    user_downloads[user_id] = 0 # تصفير العداد
    bot.answer_callback_query(call.id, "✅ تم تصفير العداد، يمكنك التحميل الآن!")
    bot.edit_message_text("🔓 تم فتح التحميل من جديد! أرسل رابط الفيديو الآن.", call.message.chat.id, call.message.message_id)

bot.infinity_polling()
