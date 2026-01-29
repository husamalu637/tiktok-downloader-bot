import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from yt_dlp import YoutubeDL

# بيانات البوت
API_TOKEN = '8235603726:AAHA14coek5rb90rLwO80vkDAMKaId2bw0g'
CHANNEL_ID = '@husam22227'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# إعدادات التحميل
YDL_OPTIONS = {
    'format': 'best',
    'outtmpl': 'video.mp4',
    'quiet': True,
}

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("أهلاً بك! أرسل رابط تيك توك وسأحمله لك فوراً ✅")

@dp.message()
async def download(message: types.Message):
    if 'tiktok.com' in message.text:
        msg = await message.answer("⏳ جاري التحميل... انتظر قليلاً")
        try:
            with YoutubeDL(YDL_OPTIONS) as ydl:
                ydl.download([message.text])
            
            video = types.FSInputFile("video.mp4")
            await message.answer_video(video, caption="تم التحميل بواسطة بوت الأنصاري ✅")
            os.remove("video.mp4")
            await msg.delete()
        except Exception as e:
            await msg.edit_text(f"❌ فشل التحميل. تأكد من الرابط.")
            print(f"Error: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
