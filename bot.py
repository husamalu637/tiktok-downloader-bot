import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from yt_dlp import YoutubeDL

# بيانات البوت
API_TOKEN = '8235603726:AAHA14coek5rb_V7S36TfN46v_XU6_W7jU'
CHANNEL_ID = '@husam22227'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# دالة التحقق من الاشتراك
async def is_subscribed(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
    except Exception:
        pass
    return False

YDL_OPTIONS = {'format': 'best', 'outtmpl': 'video.mp4', 'quiet': True}

@dp.message(Command("start"))
async def start(message: types.Message):
    if await is_subscribed(message.from_user.id):
        await message.answer("أهلاً بك! أرسل رابط تيك توك وسأحمله لك.")
    else:
        await message.answer(f"عذراً! يجب عليك الاشتراك في القناة أولاً:\n{CHANNEL_ID}")

@dp.message()
async def download(message: types.Message):
    if not await is_subscribed(message.from_user.id):
        await message.answer(f"⚠️ يرجى الاشتراك في القناة أولاً:\n{CHANNEL_ID}")
        return
    if 'tiktok.com' in message.text:
        msg = await message.answer("جاري التحميل...⏳")
        try:
            with YoutubeDL(YDL_OPTIONS) as ydl:
                ydl.download([message.text])
            video = types.FSInputFile("video.mp4")
            await message.answer_video(video, caption="تم التحميل بنجاح ✅")
            os.remove("video.mp4")
            await msg.delete()
        except Exception as e:
            await msg.edit_text(f"❌ حدث خطأ: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
