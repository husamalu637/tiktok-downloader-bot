import telebot
import yt_dlp
import os

# توكن البوت الخاص بك
TOKEN = '8235603726:AAHA14coek5rb90rLwO80vkDAMKaId2bw0g'
bot = telebot.TeleBot(TOKEN)

# معرف القناة الخاص بك
CHANNEL_LINK = "https://t.me/husam22227"

# قاموس لتخزين عدد تحميلات المستخدمين (يتم تصفيره عند إعادة تشغيل السيرفر)
user_stats = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🎬 **مرحباً بك في بوت تحميل تيك توك!**\n\n"
        "🚀 أرسل رابط الفيديو الآن لتحميله بجودة عالية.\n\n"
        "⚠️ **ملاحظة:** الحد الأقصى للحجم هو **50 ميجا**."
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def download_tiktok(message):
    user_id = message.from_user.id
    url = message.text
    
    # التحقق من عدد التحميلات
    if user_id not in user_stats:
        user_stats[user_id] = 0
    
    if user_stats[user_id] >= 5:
        sub_text = (
            "📢 **عذراً، لقد وصلت للحد المسموح (5 فيديوهات).**\n\n"
            "لدعمنا والاستمرار في استخدام البوت، يرجى الاشتراك في قناتنا أولاً:\n"
            f"👇\n{CHANNEL_LINK}\n\n"
            "بعد الاشتراك، يمكنك إكمال التحميل مجاناً! ✅"
        )
        bot.reply_to(message, sub_text, parse_mode='Markdown')
        return

    if "tiktok.com" not in url:
        bot.reply_to(message, "❌ أرسل رابط تيك توك فقط.")
        return

    msg = bot.reply_to(message, "⏳ جاري التحميل بجودة عالية...")
    
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
            info = ydl.extract_info(url, download=False)
            filesize = info.get('filesize', 0) or info.get('filesize_approx', 0)
            
            if filesize > 50 * 1024 * 1024:
                bot.edit_message_text("⚠️ الحجم يتخطى 50 ميجا!", message.chat.id, msg.message_id)
                return

            ydl.download([url])
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video, caption="✅ تم التحميل بنجاح!")
            # زيادة عدد التحميلات للمستخدم بعد النجاح
            user_stats[user_id] += 1
        
        if os.path.exists(filename):
            os.remove(filename)
        bot.delete_message(message.chat.id, msg.message_id)
        
    except Exception:
        bot.edit_message_text("❌ حدث خطأ، تأكد من الرابط.", message.chat.id, msg.message_id)
        if 'filename' in locals() and os.path.exists(filename): os.remove(filename)

bot.infinity_polling()
