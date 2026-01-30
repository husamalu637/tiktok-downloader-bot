import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import yt_dlp

# سيقوم السيرفر بقراءة التوكن من "Environment Variables"
TOKEN = os.getenv("BOT_TOKEN") 
CHANNEL_ID = '@husam22227'

def download_tiktok_sync(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video_%(id)s.mp4',
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

async def check_subscribe(user_id, context):
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['creator', 'administrator', 'member']
    except:
        return False

async def handle_message(update, context):
    user_id = update.effective_user.id
    if not await check_subscribe(user_id, context):
        keyboard = [[InlineKeyboardButton("اشترك هنا ✅", url=f"https://t.me/husam22227")]]
        await update.message.reply_text("يجب الاشتراك أولاً!", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if "tiktok.com" in update.message.text:
        msg = await update.message.reply_text("⏳ جاري التحميل...")
        try:
            file_path = await asyncio.to_thread(download_tiktok_sync, update.message.text)
            with open(file_path, 'rb') as video:
                await update.message.reply_video(video=video)
            os.remove(file_path)
            await msg.delete()
        except Exception as e:
            await msg.edit_text(f"خطأ: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
