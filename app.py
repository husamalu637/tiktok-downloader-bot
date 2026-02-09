import telebot
import yt_dlp
import os

TOKEN = '8235603726:AAHA14coek5rb90rLwO80vkDAMKaId2bw0g'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "✅ **بوت التحميل الشامل جاهز للعمل!**\n\n"
        "أرسل لي أي رابط من:\n"
        "📺 يوتيوب | 📱 تيك توك | 📸 إنستغرام | 💙 فيسبوك\n\n"
        "⚙️ الجودة المحددة: **480p** لضمان أقصى سرعة."
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    if not url.startswith('http'):
        bot.reply_to(message, "⚠️ عذراً، يجب أن ترسل رابطاً صحيحاً.")
        return

    msg = bot.reply_to(message, "🔍 جاري التحليل والتحميل من المنصة... انتظر قليلاً.")
    
    # إعدادات احترافية لدعم المنصات الأربعة بجودة 480p
    ydl_opts = {
        'format': 'best[height<=480]/bestvideo[height<=480]+bestaudio/best', # الأولوية لـ 480p
        'outtmpl': 'video_%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'add_header': [
            'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # استخراج المعلومات والتحميل
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # التأكد من امتداد الملف إذا تغير بعد التحميل
            if not os.path.exists(filename):
                filename = filename.rsplit('.', 1)[0] + ".mp4"

        with open(filename, 'rb') as video:
            bot.send_video(
                message.chat.id, 
                video, 
                caption=f"✅ تم التحميل بنجاح بجودة 480p\n🔗 الرابط: {url}"
            )
        
        # تنظيف السيرفر فوراً لتوفير مساحة Koyeb
        os.remove(filename)
        bot.delete_message(message.chat.id, msg.message_id)
        
    except Exception as e:
        error_msg = "❌ فشل التحميل. قد يكون:\n1- الحساب خاص (Private).\n2- الرابط غير صحيح.\n3- الفيديو محمي بحقوق طبع ونشر."
        bot.edit_message_text(error_msg, message.chat.id, msg.message_id)
        # تنظيف أي ملف معلق في حال الخطأ
        for f in os.listdir():
            if f.startswith("video_"): os.remove(f)

bot.infinity_polling()
