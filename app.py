import telebot
import yt_dlp
import os

# توكن البوت الخاص بك
TOKEN = '8235603726:AAHA14coek5rb90rLwO80vkDAMKaId2bw0g'
bot = telebot.TeleBot(TOKEN)

# معرف القناة (يجب أن يبدأ بـ @)
CHANNEL_ID = "@husam22227"
CHANNEL_LINK = "https://t.me/husam22227"

def is_subscribed(user_id):
    try:
        # التحقق من حالة المستخدم في القناة
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        # إذا كان مشرف، مالك، أو عضو عادي
        return status in ['member', 'administrator', 'creator']
    except Exception:
        # في حال حدوث خطأ (مثل أن البوت ليس مشرفاً) سنعتبره غير مشترك للأمان
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🎬 **مرحباً بك في بوت تحميل تيك توك!**\n\n"
        "🚀 أرسل رابط الفيديو الآن لتحميله بجودة عالية.\n\n"
        "✅ اشترك مرة واحدة في قناتنا للاستخدام الدائم:\n"
        f"{CHANNEL_LINK}"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def download_tiktok(message):
    user_id = message.from_user.id
    url = message.text
    
    # 1. التحقق من الاشتراك الإجباري
    if not is_subscribed(user_id):
        sub_text = (
            "⚠️ **عذراً، يجب عليك الاشتراك في القناة أولاً!**\n\n"
            "اشترك هنا ثم أرسل الرابط مرة أخرى:\n"
            f"👇\n{CHANNEL_LINK}\n\n"
            "✅ الاشتراك مطلوب لمرة واحدة فقط لضمان عمل البوت معك دائماً."
        )
        bot.reply_to(message, sub_text, parse_mode='Markdown')
        return

    # 2. التحقق من الرابط
    if "tiktok.com" not in url:
        bot.reply_to(message, "❌ أرسل رابط تيك توك فقط.")
        return

    msg = bot.reply_to(message, "⏳ جاري التحميل بجودة عالية... انتظر قليلاً.")
    
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
            # فحص الحجم قبل التحميل
            info = ydl.extract_info(url, download=False)
            filesize = info.get('filesize', 0) or info.get('filesize_approx', 0)
            
            if filesize > 50 * 1024 * 1024:
                bot.edit_message_text("⚠️ حجم الفيديو أكبر من 50 ميجا!", message.chat.id, msg.message_id)
                return

            ydl.download([url])
            filename = ydl.prepare_filename(info)

        # 3. إرسال الفيديو
        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video, caption="✅ تم التحميل بنجاح!\n\nشكراً لاشتراكك في قناتنا.")
        
        if os.path.exists(filename):
            os.remove(filename)
        bot.delete_message(message.chat.id, msg.message_id)
        
    except Exception:
        bot.edit_message_text("❌ حدث خطأ، تأكد من أن الفيديو عام وليس خاصاً.", message.chat.id, msg.message_id)
        if 'filename' in locals() and os.path.exists(filename): os.remove(filename)

bot.infinity_polling()
