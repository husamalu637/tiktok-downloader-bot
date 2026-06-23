import telebot
import yt_dlp
import os
import uuid
import re
import time

# التوكن الخاص بك
TOKEN = '8235603726:AAHA14coek5rb90rLwO80vkDAMKaId2bw0g'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = (
        "مرحباً بك في بوت تحميل الفيديوهات\n\n"
        "أرسل رابط الفيديو لتحميله\n\n"
        "المنصات المدعومة\n"
        "يوتيوب\n"
        "تيك توك\n"
        "فيسبوك\n"
        "إنستغرام\n\n"
        "ملاحظة\n"
        "الحد الأقصى لحجم الفيديو هو 50 ميجا"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_download(message):
    url_match = re.search(r'(https?://[^\s]+)', message.text)
    if not url_match:
        return

    url = url_match.group(0)
    
    supported = ["tiktok.com", "facebook.com", "fb.watch", "fb.com", "youtube.com", "youtu.be", "instagram.com"]
    
    if not any(x in url for x in supported):
        bot.reply_to(message, "الرابط المرسل غير مدعوم")
        return

    msg = bot.reply_to(message, "جاري بدء التحميل...")
    
    filename = f'vid_{uuid.uuid4().hex[:8]}.mp4'
    
    # دالة مراقبة وتحديث عداد التحميل في تليجرام
    last_update_time = time.time()
    
    def progress_hook(d):
        nonlocal last_update_time
        if d['status'] == 'downloading':
            # لتجنب إرسال طلبات تحديث كثيرة وحظر البوت من تليجرام، نحدث الرسالة كل ثانيتين فقط
            current_time = time.time()
            if current_time - last_update_time > 2.0:
                percent = d.get('_percent_str', '0%').strip()
                # تنظيف النص من الألوان والأشرطة الغريبة لـ تليجرام
                percent = re.sub(r'\x1b\[[0-9;]*m', '', percent) 
                
                downloaded = d.get('_downloaded_bytes_str', '0B')
                total = d.get('_total_bytes_str', d.get('_total_bytes_estimate_str', 'غير معروف'))
                
                try:
                    bot.edit_message_text(
                        f"⏳ جاري التحميل الآن...\n\n"
                        f"📊 النسبة: {percent}\n"
                        f"📥 المحمل: {downloaded} من {total}",
                        message.chat.id, msg.message_id
                    )
                except Exception:
                    pass  # لتخطي خطأ تليجرام إذا كان النص متطابقاً
                last_update_time = current_time
        elif d['status'] == 'finished':
            try:
                bot.edit_message_text("✅ اكتمل التحميل، جاري إرسال الفيديو الآن...", message.chat.id, msg.message_id)
            except Exception:
                pass

    ydl_opts = {
        'format': 'best[ext=mp4]/best', 
        'outtmpl': filename,
        'quiet': True,
        'max_filesize': 52428800, # 50MB
        'no_warnings': True,
        'socket_timeout': 30,
        'progress_hooks': [progress_hook], # ربط دالة العداد بـ yt-dlp
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
    }

    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            with open(filename, 'rb') as video:
                bot.send_video(message.chat.id, video, caption="تم التحميل بنجاح")
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("❌ تعذر حفظ الملف أو تجاوز الحد المسموح", message.chat.id, msg.message_id)
            
    except yt_dlp.utils.MaxFileSizeReached:
        bot.edit_message_text("❌ الملف يتجاوز حد الـ 50 ميجا", message.chat.id, msg.message_id)
    except Exception as e:
        print(f"Error: {str(e)}")
        bot.edit_message_text("❌ حدث خطأ أو حظر من المنصة! يرجى المحاولة لاحقاً.", message.chat.id, msg.message_id)
    
    finally:
        if os.path.exists(filename):
            os.remove(filename)

# تنظيف الجلسات والبدء
bot.delete_webhook()
print("🚀 البوت يعمل الآن مع العداد بنجاح...")
bot.infinity_polling()
