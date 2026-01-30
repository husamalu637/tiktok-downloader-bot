import os
import aiohttp
from aiogram import Bot, Dispatcher, executor, types

# وضع التوكن الخاص بك هنا
API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("✅ أهلاً بك! أرسل لي رابط تيك توك وسأقوم بتحميله فوراً.")

@dp.message_handler()
async def handle_video(message: types.Message):
    url = message.text
    if "tiktok.com" in url:
        msg = await message.answer("⏳ جاري التحميل...")
        try:
            # المحرك السريع الذي استخدمناه صباحاً
            async with aiohttp.ClientSession() as session:
                api_url = f"https://www.tikwm.com/api/?url={url}"
                async with session.get(api_url) as resp:
                    data = await resp.json()
                    if data.get('code') == 0:
                        video_url = "https://www.tikwm.com" + data['data']['play']
                        await message.answer_video(video_url, caption="✅ تم التحميل بنجاح")
                        await msg.delete()
                    else:
                        await msg.edit_text("❌ فشل الجلب: تأكد من أن الرابط صحيح.")
        except Exception:
            await msg.edit_text("❌ حدث خطأ فني، حاول مرة أخرى.")
    else:
        await message.reply("⚠️ أرسل رابط تيك توك فقط.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

