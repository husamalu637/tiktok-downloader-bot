import asyncio
import requests
import time
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# التوكن الجديد الخاص بك
API_TOKEN = "8235603726:AAHA14coek5rb90rLwO80vkDAMKaId2bw0g"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# إعدادات المتصفح للتمويه وتجنب الحظر
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.reply("🚀 البوت عاد للعمل بأقوى نظام اتصال! أرسل رابط تيك توك الآن.")

@dp.message()
async def download_handler(message: types.Message):
    url = message.text
    if "tiktok.com" in url:
        msg = await message.answer("⏳ جاري سحب الفيديو... يرجى الانتظار ثواني.")
        
        # المحاولة عبر المحرك الأول (TikWM) باستخدام requests
        try:
            api_url = f"https://www.tikwm.com/api/?url={url}"
            response = requests.get(api_url, headers=HEADERS, timeout=15).json()
            
            if response.get('code') == 0:
                video_url = "https://www.tikwm.com" + response['data']['play']
                await message.answer_video(video_url, caption="✅ تم التحميل بواسطة المحرك الرئيسي")
                return await msg.delete()
        except Exception as e:
            print(f"Engine 1 failed: {e}")

        # المحاولة عبر المحرك الثاني (Tiklydown) إذا فشل الأول
        try:
            await msg.edit_text("⏳ المحرك الأول مضغوط، أجرب المحرك الثاني...")
            alt_api = f"https://api.tiklydown.eu.org/api/download?url={url}"
            alt_response = requests.get(alt_api, headers=HEADERS, timeout=15).json()
            
            video_url = alt_response.get('result', {}).get('video', {}).get('noWatermark')
            if video_url:
                await message.answer_video(video_url, caption="✅ تم التحميل بواسطة المحرك الاحتياطي")
                return await msg.delete()
        except Exception as e:
            print(f"Engine 2 failed: {e}")
            
        await msg.edit_text("❌ عذراً، جميع المحركات تواجه ضغطاً حالياً. جرب الرابط بعد دقائق.")
    else:
        await message.reply("⚠️ يرجى إرسال رابط تيك توك صحيح.")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print("--- البوت يعمل الآن بقوة على السيرفر ---")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
            
