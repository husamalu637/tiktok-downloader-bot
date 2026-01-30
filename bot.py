import asyncio
import requests
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# التوكن الجديد الخاص بك (يفضل وضعه في Environment Variables في Koyeb)
API_TOKEN = "8235603726:AAHA14coek5rb90rLwO80vkDAMKaId2bw0g"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.reply("🚀 البوت عاد للخدمة من السيرفر! أرسل رابط تيك توك الآن.")

@dp.message()
async def download_handler(message: types.Message):
    url = message.text
    if "tiktok.com" in url:
        msg = await message.answer("⏳ جاري التحميل من السيرفر...")
        try:
            # استخدام API بديل ومستقر
            api_url = f"https://www.tikwm.com/api/?url={url}"
            response = requests.get(api_url).json()
            
            if response.get('code') == 0:
                video_url = "https://www.tikwm.com" + response['data']['play']
                
                # تحميل الفيديو وإرساله كملف لتجنب مشاكل الروابط
                video_data = requests.get(video_url).content
                video_file = types.BufferedInputFile(video_data, filename="video.mp4")
                
                await message.answer_video(video_file, caption="✅ تم التحميل بواسطة سيرفرك الخاص")
                await msg.delete()
            else:
                await msg.edit_text("❌ لم يتم العثور على الفيديو، قد يكون الرابط خاطئاً.")
        except Exception as e:
            await msg.edit_text("⚠️ السيرفر واجه ضغطاً، حاول مرة أخرى بعد قليل.")
    else:
        await message.reply("⚠️ يرجى إرسال رابط تيك توك صحيح.")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
                
