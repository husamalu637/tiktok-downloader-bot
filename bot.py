import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# التوكن الخاص بك
API_TOKEN = "8235603726:AAHA14coek5rb90rLwO80vkDAMKaId2bw0g"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.reply("🚀 البوت يعمل بـ 3 محركات تحميل عالمية! أرسل الرابط.")

@dp.message()
async def download(message: types.Message):
    url = message.text
    if "tiktok.com" in url:
        msg = await message.answer("⏳ جاري محاولة التحميل من 3 مصادر...")
        
        # --- المحرك 1: TikWM ---
        try:
            res = requests.get(f"https://www.tikwm.com/api/?url={url}", headers=HEADERS, timeout=10).json()
            if res.get('code') == 0:
                return await message.answer_video("https://www.tikwm.com" + res['data']['play'], caption="✅ المصدر 1")
        except: pass

        # --- المحرك 2: Tiklydown ---
        try:
            res = requests.get(f"https://api.tiklydown.eu.org/api/download?url={url}", timeout=10).json()
            video = res.get('result', {}).get('video', {}).get('noWatermark')
            if video:
                return await message.answer_video(video, caption="✅ المصدر 2")
        except: pass

        # --- المحرك 3: TTDL (المحرك السري) ---
        try:
            res = requests.get(f"https://api.vkrhost.com/api/tiktok?url={url}", timeout=10).json()
            video = res.get('data', {}).get('video')
            if video:
                return await message.answer_video(video, caption="✅ المصدر 3")
        except: pass

        await msg.edit_text("❌ جميع المصادر محظورة حالياً في السيرفر. جرب رابطاً آخر أو انتظر قليلاً.")
    else:
        await message.reply("⚠️ أرسل رابط تيك توك صحيح.")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    
