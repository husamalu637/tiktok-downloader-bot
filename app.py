import os
# --- الميزة 1: تحديث المكتبة تلقائياً عند التشغيل على السيرفر لضمان عمل يوتيوب ---
os.system("pip install -U yt-dlp")

import telebot
import yt_dlp
import uuid
import re
from telebot import types

# التوكن الخاص بك
TOKEN = '8235603726:AAHA14coek5rb90rLwO80vkDAMKaId2bw0g'
bot = telebot.TeleBot(TOKEN)

# رابط الإعلانات للدعم
SUPPORT_LINK = "https://www.effectivegatecpm.com/xaeg3i863?key=23cf5c1f0aa47c762d8b1fc9de714230"

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("☕ لدعم استمرار البوت", url=SUPPORT_LINK))
    
    bot.reply_to(message, 
        "🎬 **مرحباً بك في بوت التحميل المطور!**\n\n"
        "🚀 **البوت يدعم التحميل من:**\n"
        "✅ يوتيوب (YouTube)\n"
        "✅ إنستغرام (Instagram)\n"
        "✅ تيك توك (TikTok)\n"
        "✅ فيسبوك (Facebook)\n\n"
        "⚠️ **تنبيه:** الحد الأقصى للحجم هو **50 ميجا**.\n"
        "أرسل رابط الفيديو الآن لنبدأ!", 
        reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_download(message):
    # البحث عن الرابط
    url_match = re.search(r'(https?://[^\s]+)', message.text)
    if not url_match:
        return

    url = url_match.group(0)
    
    # --- الميزة 2: تم تعديل القائمة المسموحة لتشمل يوتيوب وإنستغرام ---
    supported = ["tiktok.com", "facebook.com", "fb.watch", "fb.com", "youtube.com", "youtu.be", "instagram.com"]
    
    if not any(x in url for x in supported):
        bot.reply_to(message, "❌ **عذراً!** هذا البوت يدعم التحميل من (يوتيوب، إنستغرام، تيك توك، فيسبوك) فقط.")
        return

    msg = bot.reply_to(message, "⏳ جاري التحميل ومعالجة الرابط...\n(تذكر: الحد الأقصى 50MB)")
    
    filename = f'vid_{uuid.uuid4().hex[:8]}.mp4'
    
    # --- الميزة 3: تطوير إعدادات التحميل لضمان دمج الصوت والصورة وتخطي الحماية ---
    ydl_opts = {
        'format': 'best[ext=mp4]/best', # اختيار أفضل جودة بصيغة mp4 لضمان عمل الصوت
        'outtmpl': filename,
        'quiet': True,
        'max_filesize': 52428800, # 50MB
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        if os.path.exists(filename):
            with open(filename, 'rb') as video:
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("☕ دعم البوت", url=SUPPORT_LINK))
                bot.send_video(message.chat.id, video, caption="✅ تم التحميل بنجاح!", reply_markup=markup)
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("❌ الفيديو أكبر من 50 ميجا أو لم يتم العثور عليه.", message.chat.id, msg.message_id)
            
    except Exception as e:
        # طباعة الخطأ في الكونسول للمطور للمساعدة في التشخيص
        print(f"Error: {e}")
        bot.edit_message_text("❌ حدث خطأ! تأكد أن الرابط عام وليس خاصاً.", message.chat.id, msg.message_id)
    
    finally:
        if os.path.exists(filename):
            os.remove(filename)

# تنظيف الجلسات والبدء
bot.delete_webhook()
print("🚀 البوت يعمل الآن (YouTube + Instagram + TikTok + Facebook)...")
bot.infinity_polling()
