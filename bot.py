
import telebot
import yt_dlp
import os

# توكن البوت الخاص بك
TOKEN = '8235603726:AAHA14coek5rb90rLwO80vkDAMKaId2bw0g'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✅ أهلاً بك! البوت يعمل الآن على خوادم Koyeb.\nأرسل لي رابط فيديو من تيك توك، يوتيوب، إنستغرام، أو فيسبوك للتحميل بجودة 480p.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    if not url.startswith('http'):
        bot.reply_to(message, "⚠️ من فضلك أرسل رابطاً صحيحاً يبدأ بـ http")
        return

    msg = bot.reply_to(message, "⏳ جاري المعالجة والتحميل... يرجى الانتظار.")
    
    # خيارات yt-dlp للجودة والتحميل
    ydl_opts = {
        'format': 'best[height<=480]', 
        'outtmpl': 'video.mp4',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        with open('video.mp4', 'rb') as video:
            bot.send_video(message.chat.id, video, caption="تم التحميل بواسطة بوتك الخاص 🤖")
        
        os.remove('video.mp4')
        bot.delete_message(message.chat.id, msg.message_id)
        
    except Exception as e:
        bot.reply_to(message, "❌ حدث خطأ! قد يكون الفيديو خاصاً أو الرابط غير مدعوم.")
        if os.path.exists('video.mp4'): os.remove('video.mp4')

bot.infinity_polling()
