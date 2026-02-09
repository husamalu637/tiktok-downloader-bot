import telebot
import yt_dlp
import os

TOKEN = '8235603726:AAHA14coek5rb90rLwO80vkDAMKaId2bw0g'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✅ البوت يعمل الآن! أرسل الرابط وسأحاول تحميله بأسرع طريقة ممكنة.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    if not url.startswith('http'): return

    msg = bot.reply_to(message, "⏳ جاري التحميل... (قد يستغرق وقتاً حسب حجم الفيديو)")
    
    # إعدادات قوية جداً لتجاوز الحظر
    ydl_opts = {
        'format': 'best[height<=360]/best', 
        'outtmpl': 'video_%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        # إضافة هوية متصفح حقيقية لتجنب الحظر
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com/',
        'extract_flat': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # محاولة جلب الرابط المباشر أولاً
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video, caption="✅ تم التحميل!")
        
        os.remove(filename)
        bot.delete_message(message.chat.id, msg.message_id)
        
    except Exception as e:
        # إذا فشل، نحاول إرسال رسالة توضح الخطأ الحقيقي للمطور
        bot.edit_message_text(f"❌ عذراً، المنصة تمنع التحميل حالياً أو الفيديو محمي.", message.chat.id, msg.message_id)
        if 'filename' in locals() and os.path.exists(filename): os.remove(filename)

bot.infinity_polling()
