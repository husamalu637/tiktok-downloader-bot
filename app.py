import telebot
import yt_dlp
import os

# توكن البوت الخاص بك
TOKEN = '8235603726:AAHA14coek5rb90rLwO80vkDAMKaId2bw0g'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "✅ **تم تفعيل البوت بنجاح!**\n\n"
        "أرسل لي أي رابط فيديو من:\n"
        "📺 YouTube | 📱 TikTok | 📸 Instagram | 💙 Facebook\n\n"
        "⚡️ تم ضبط الجودة على **360p** لضمان سرعة التحميل."
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    if not url.startswith('http'):
        return

    msg = bot.reply_to(message, "⏳ جاري المعالجة والتحميل بسرعة قصوى...")
    
    # إعدادات مخففة (360p) لضمان عدم توقف السيرفر
    ydl_opts = {
        'format': 'best[height<=360]/best', 
        'outtmpl': 'vid_%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # التأكد من المسار الصحيح للملف
            if not os.path.exists(filename):
                filename = filename.rsplit('.', 1)[0] + ".mp4"

        with open(filename, 'rb') as video:
            bot.send_video(
                message.chat.id, 
                video, 
                caption=f"✅ تم التحميل بنجاح (360p)\n🔗 {url}"
            )
        
        # حذف الملف فوراً لتوفير مساحة السيرفر
        os.remove(filename)
        bot.delete_message(message.chat.id, msg.message_id)
        
    except Exception as e:
        bot.edit_message_text("❌ فشل التحميل. قد يكون الفيديو خاصاً أو الرابط غير مدعوم حالياً.", message.chat.id, msg.message_id)
        # تنظيف أي ملفات عالقة في حال الخطأ
        for f in os.listdir():
            if f.startswith("vid_"): os.remove(f)

bot.infinity_polling()
