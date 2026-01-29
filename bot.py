import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from yt_dlp import YoutubeDL

# بيانات البوت الأساسية
API_TOKEN = '8235603726:AAHA14coek5rb_V7S36TfN46v_XU6_W7jU'
CHANNEL_ID = '@husam22227'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# دالة التحقق من الاشتراك (هذه هي التي تمنع غير المشتركين)
async def is_subscribed(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
        return False
    except Exception as e:
        print(f"Error checking subscription: {e}")
        return False

# إعدادات التحميل
YDL_OPTIONS = {
    'format': 'best',
    'outtmpl': 'video.mp4',
    'quiet': True,
}

@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    if await is_subscribed(user_id):
        await message.answer("✅ أهلاً بك! أنت مشترك في القناة. أرسل رابط تيك توك للتحميل.")
    else:
        await message.answer(f"⚠️ عذراً! يجب عليك الاشتراك في القناة أولاً لتتمكن من استخدام البوت:\n\n{CHANNEL_ID}\n\nبعد الاشتراك أرسل /start")

@dp.message()
async def download(message: types.Message):
    user_id = message.from_user.id
    
    # التحقق من الاشتراك قبل أي عملية تحميل
    if not await is_subscribed(user_id):
        await message.answer(f"❌ لا يمكنك التحميل! اشترك في القناة أولاً:\n\n{CHANNEL_ID}")
        return

    # إذا كان الرابط من تيك توك
    if 'tiktok.com' in message.text:
        msg = await message.answer("جاري التحميل... ⏳")
        try:
            with YoutubeDL(YDL_OPTIONS) as ydl:
                ydl.download([message.text])
            
            video = types.FSInputFile("video.mp4")
            await message.answer_video(video, caption="تم التحميل بنجاح ✅")
            
            # حذف الفيديو من السيرفر بعد الإرسال لتوفير المساحة
            if os.path.exists("video.mp4"):
                os.remove("video.mp4")
            await msg.delete()
        except Exception as e:
            await msg.edit_text(f"❌ حدث خطأ أثناء التحميل. تأكد من الرابط.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    
