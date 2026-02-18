import telebot
import yt_dlp
import os
import uuid
import re
from telebot import types

# التوكن الخاص بك
TOKEN = '8235603726:AAHA14coek5rb90rLwO80vkDAMKaId2bw0g'
bot = telebot.TeleBot(TOKEN)

SUPPORT_LINK = "https://www.effectivegatecpm.com/xaeg3i863?key=23cf5c1f0aa47c762d8b1fc9de714230"

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("☕ لدعم استمرار البوت", url=SUPPORT_LINK))
    
    bot.reply_to(message, 
        "🎬 **مرحباً بك في بوت التحميل الشامل!**\n\n"
        "🚀 **يدعم الآن:**\n"
        "✅ يوتيوب و إنستغرام\n"
        "✅ تيك توك و فيسبوك\n\n"
        "أرسل الرابط وسأقوم بالتحميل فوراً!", 
        reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_download(message):
    url_match = re.search(r'(https?://[^\s]+)', message.text)
    if not url_match: return

    url = url_match.group(0)
    msg = bot.reply_to(message, "⏳ جاري التحميل... يرجى الانتظار.")
    
    filename = f'vid_{uuid.uuid4().hex[:8]}.mp4'
    
    ydl_opts = {
        # 'best' هي الأضمن للعمل على Koyeb لتجنب مشاكل المعالجة الثقيلة
        'format': 'best[ext=mp4]/best',
        'outtmpl': filename,
        'quiet': True,
        'no_warnings': True,
        'max_filesize': 50 * 1024 * 1024, # 50MB
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        if os.path.exists(filename):
            with open(filename, 'rb') as video:
                bot.send_video(message.chat.id, video, caption="✅ تم التحميل بنجاح!")
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("❌ لم أتمكن من العثور على الفيديو، قد يكون خاصاً أو كبيراً جداً.", message.chat.id, msg.message_id)
            
    except Exception as e:
        bot.edit_message_text(f"❌ حدث خطأ أثناء التحميل. تأكد من صحة الرابط.", message.chat.id, msg.message_id)
    
    finally:
        if os.path.exists(filename):
            os.remove(filename)

# تشغيل البوت بنظام لا يتوقف
if __name__ == '__main__':
    print("🚀 البوت يعمل الآن على Koyeb...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
    
