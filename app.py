
Import telebot
import yt_dlp
import os

# توكن البوت الخاص بك
TOKEN = '8235603726:AAHA14coek5rb90rLwO80vkDAMKaId2bw0g'
bot = telebot.TeleBot(TOKEN)

# معرف القناة الخاص بك للإعلان
CHANNEL_USER = "@husam22227"
CHANNEL_LINK = "https://t.me/husam22227"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🎬 **مرحباً بك في بوت تحميل تيك توك!**\n\n"
        "🚀 أرسل رابط الفيديو الآن لتحميله بجودة عالية.\n\n"
        f"📢 تابع جديدنا على: {CHANNEL_USER}"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def download_tiktok(message):
    url = message.text
    user_id = message.from_user.id
    
    # التأكد أن الرابط تيك توك
    if "tiktok.com" not in url:
        bot.reply_to(message, f"❌ أرسل رابط تيك توك فقط.\n\nلمتابعة شروحاتنا: {CHANNEL_USER}")
        return

    msg = bot.reply_to(message, "⏳ جاري التحميل... انتظر قليلاً")
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'vid_{user_id}.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # فحص الحجم (50 ميجا)
            info = ydl.extract_info(url, download=False)
            filesize = info.get('filesize', 0) or info.get('filesize_approx', 0)
            
            if filesize > 50 * 1024 * 1024:
                bot.edit_message_text(f"⚠️ الفيديو ضخم جداً (أكبر من 50MB)!\n\nقناتنا: {CHANNEL_USER}", message.chat.id, msg.message_id)
                return

            ydl.download([url])
            filename = ydl.prepare_filename(info)

        # إرسال الفيديو مع الإعلان في الوصف (Caption)
        with open(filename, 'rb') as video:
            caption_text = (
                "✅ تم التحميل بنجاح!\n\n"
                f"🚀 بواسطة: @{bot.get_me().username}\n"
                f"📢 تابع قناتنا: {CHANNEL_USER}"
            )
            bot.send_video(message.chat.id, video, caption=caption_text)
        
        # تنظيف السيرفر
        if os.path.exists(filename):
            os.remove(filename)
        bot.delete_message(message.chat.id, msg.message_id)
        
    except Exception:
        bot.edit_message_text(f"❌ فشل التحميل. تأكد من الرابط.\n\nللدعم: {CHANNEL_USER}", message.chat.id, msg.message_id)
        if 'filename' in locals() and os.path.exists(filename): os.remove(filename)

bot.infinity_polling()
