import os
import logging
import yt_dlp
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@husam22227"
CHANNEL_URL = "https://t.me/husam22227"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# خيارات مكتبة yt-dlp لجلب الفيديو بأقل استهلاك للموارد
YDL_OPTIONS = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'quiet': True,
    'no_warnings': True,
}

async def is_sub(user_id):
    try:
        m = await bot.get_chat_member(CHANNEL_ID, user_id)
        return m.status in ['member', 'administrator', 'creator']
    except: return True

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if await is_sub(message.from_user.id):
        await message.reply("✅ البوت يعمل الآن باستخدام المكتبات الداخلية. أرسل الرابط!")
    else:
        kb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("إشترك هنا 📢", url=CHANNEL_URL))
        await message.reply(f"⚠️ اشترك أولاً:\n{CHANNEL_ID}", reply_markup=kb)

@dp.message_handler()
async def download_video(message: types.Message):
    if not await is_sub(message.from_user.id): return await start(message)

    url = message.text
    if "tiktok.com" in url:
        msg = await message.reply("⏳ جاري المعالجة بواسطة المكتبة البرمجية...")
        try:
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                video_url = info.get('url')
                
                if video_url:
                    await message.answer_video(video_url, caption="✅ تم التحميل عبر yt-dlp")
                    await msg.delete()
                else:
                    raise Exception("لم يتم العثور على رابط")
        except Exception as e:
            logging.error(f"Error: {e}")
            await msg.edit_text("❌ المكتبة واجهت مشكلة في فك تشفير الرابط، قد يكون الفيديو محمياً.")
    else:
        await message.reply("⚠️ أرسل رابط تيك توك صحيح.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
