import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# التوكن الجديد والمفعل الخاص بك
API_TOKEN = "8235603726:AAHA14coek5rb90rLwO80vkDAMKaId2bw0g"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# رأس طلب لتبدو وكأنك متصفح حقيقي لتجنب الحظر
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.reply("🚀 تم تحديث البوت بالتوكن الجديد! أرسل رابط تيك توك وسأقوم بجلب الفيديو لك.")

@dp.message()
async def download_handler(message: types.Message):
    url = message.text
    if "tiktok.com" in url:
        msg = await message.answer("⏳ جاري جلب الرابط المباشر...")
        try:
            async with aiohttp.ClientSession(headers=HEADERS) as session:
                # طلب البيانات من المحرك (API)
                api_link = f"https://www.tikwm.com/api/?url={url}"
                async with session.get(api_link) as r:
                    res = await r.json()
                    
                    if res.get('code') == 0:
                        # استخراج رابط الفيديو المباشر
                        video_url = "https://www.tikwm.com" + res['data']['play']
                        # إرسال الرابط مباشرة لتلجرام لتوفير مساحة الرام (256MB)
                        await message.answer_video(video_url, caption="✅ تم التحميل بنجاح!")
                        await msg.delete()
                    else:
                        await msg.edit_text("❌ لم يتم العثور على الفيديو، تأكد أن الحساب ليس خاصاً.")
        except Exception as e:
            # طباعة الخطأ في السجلات للتأكد من حالة الاتصال
            print(f"Error: {e}")
            await msg.edit_text("⚠️ حدث خطأ في الاتصال، حاول مرة أخرى بعد قليل.")
    else:
        await message.reply("⚠️ من فضلك أرسل رابط تيك توك صحيح.")

async def main():
    # حذف أي رسائل قديمة معلقة لتجنب تعارض التوكن
    await bot.delete_webhook(drop_pending_updates=True)
    print("--- البوت يعمل الآن بالتوكن الجديد ---")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    
