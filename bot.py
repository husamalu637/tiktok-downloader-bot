import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
import yt_dlp

# الإعدادات
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = '@husam22227'

async def check_subscribe(user_id, context):
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['creator', 'administrator', 'member']
    except:
        return False

# --- وظيفة الترحيب عند الضغط على Start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"أهلاً بك يا {user_name} في بوت تحميل تيك توك! 📥\n\n"
        "من فضلك، أرسل رابط الفيديو الآن وسأقوم بتحميله لك فوراً."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text
    
    # التحقق من الاشتراك
    if not await check_subscribe(user_id, context):
        keyboard = [[InlineKeyboardButton("اضغط هنا للاشتراك في القناة ✅", url=f"https://t.me/husam22227")]]
        await update.message.reply_text(
            "⚠️ عذراً، يجب عليك الاشتراك في القناة أولاً لاستخدام البوت.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    # معالجة الرابط
    if "tiktok.com" in user_text:
        msg = await update.message.reply_text("⏳ جاري معالجة الفيديو، انتظر قليلاً...")
        try:
            # دالة التحميل (نفس التي استخدمناها سابقاً)
            loop = asyncio.get_event_loop()
            file_path = await loop.run_in_executor(None, lambda: download_tiktok_sync(user_text))
            
            with open(file_path, 'rb') as video:
                await update.message.reply_video(video=video, caption="تم التحميل بواسطة بوتك @husam22227 ✅")
            
            os.remove(file_path)
            await msg.delete()
        except Exception as e:
            await msg.edit_text(f"❌ حدث خطأ أثناء التحميل: {e}")
    else:
        await update.message.reply_text("عذراً، أرسل رابط تيك توك صحيح فقط.")

def download_tiktok_sync(url):
    ydl_opts = {'format': 'best', 'outtmpl': 'video_%(id)s.mp4', 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

def main():
    app = Application.builder().token(TOKEN).build()
    
    # إضافة أمر ستارت
    app.add_handler(CommandHandler("start", start))
    
    # إضافة معالج الرسائل
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("البوت يعمل الآن...")
    app.run_polling()

if __name__ == '__main__':
    main()
