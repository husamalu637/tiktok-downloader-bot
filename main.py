import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# --- الإعدادات ---
TOKEN = '8235603726:AAHA14coek5rb90rLwO80vkDAMKaId2bw0g'
ADMIN_ID = 8596496166 
USERS_FILE = "users_list.txt"

def save_user(user_id):
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f: f.write(f"{user_id}\n")
    else:
        with open(USERS_FILE, "r") as f: users = f.read().splitlines()
        if str(user_id) not in users:
            with open(USERS_FILE, "a") as f: f.write(f"{user_id}\n")

async def send_online_notice(app: Application):
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            users = f.read().splitlines()
        for u_id in users:
            try:
                await app.bot.send_message(
                    chat_id=int(u_id), 
                    text="✅ أبشركم! البوت عاد للعمل الآن ومستعد لتحميل فيديوهاتكم من (فيس بوك، تيك توك، يوتيوب، إنستغرام)."
                )
                await asyncio.sleep(0.1)
            except: continue

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_user(update.message.from_user.id)
    welcome_msg = (
        "🚀 **مرحباً بك!**\n\n"
        "أنا أستطيع تحميل الفيديوهات من:\n"
        "🔹 **يوتيوب** (YouTube)\n"
        "🔹 **تيك توك** (TikTok)\n"
        "🔹 **فيس بوك** (Facebook)\n"
        "🔹 **إنستغرام** (Instagram)\n\n"
        "⚠️ **ملاحظة:** الحد الأقصى لحجم الفيديو هو 50 ميجا.\n"
        "فقط أرسل الرابط وسأقوم بالواجب! 📥"
    )
    await update.message.reply_text(welcome_msg, parse_mode='Markdown')

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    save_user(user_id)
    url = update.message.text
    status_msg = await update.message.reply_text('⏳ جاري المعالجة... انتظر قليلاً')

    ydl_opts = {
        'format': 'best',
        'outtmpl': f'video_{user_id}.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as video:
            await context.bot.send_video(chat_id=user_id, video=video, caption=f"✅ تم التحميل بنجاح!")
        
        if os.path.exists(filename): os.remove(filename)
        await status_msg.delete()
    except Exception:
        await status_msg.edit_text("❌ تعذر التحميل. تأكد من الرابط والحجم (أقل من 50 ميجا).")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    try:
        loop = asyncio.get_event_loop()
        loop.create_task(send_online_notice(app))
    except: pass

    print("البوت يعمل...")
    app.run_polling()

if __name__ == '__main__':
    main()
