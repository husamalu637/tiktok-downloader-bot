
import os
import aiohttp
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@husam22227"
CHANNEL_URL = "https://t.me/husam22227"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def is_sub(user_id):
    try:
        m = await bot.get_chat_member(CHANNEL_ID, user_id)
        return m.status in ['member', 'administrator', 'creator']
    except: return True

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if await is_sub(message.from_user.id):
        await message.reply("✅ أهلاً بك! أرسل رابط تيك توك الآن.")
    else:
        kb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("إشترك هنا 📢", url=CHANNEL_URL))
        await message.reply(f"⚠️ اشترك أولاً في القناة لتتمكن من التحميل:\n{CHANNEL_ID}", reply_markup=kb)

@dp.message_handler()
async def download(message: types.Message):
    if not await is_sub(message.from_user.id):
        return await start(message)

    url = message.text
    if "tiktok.com" in url:
        msg = await message.reply("⏳ جاري جلب الفيديو...")
        try:
            # استخدام محرك Tiklydown البديل (أكثر استقراراً حالياً)
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.tiklydown.eu.org/api/download?url={url}") as r:
                    res = await r.json()
                    # استخراج الفيديو بدون علامة مائية
                    video = res['result']['video']['noWatermark']
                    await message.answer_video(video, caption="✅ تم التحميل بنجاح!")
                    await msg.delete()
        except:
            # محاولة أخيرة بمحرك Tikwm إذا فشل الأول
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://www.tikwm.com/api/?url={url}") as r:
                        res = await r.json()
                        video = "https://www.tikwm.com" + res['data']['play']
                        await message.answer_video(video, caption="✅ تم التحميل (محرك 2)")
                        await msg.delete()
            except:
                await msg.edit_text("❌ الخدمة مضغوطة حالياً، حاول مرة أخرى بعد قليل.")
    else:
        await message.reply("⚠️ أرسل رابط تيك توك صحيح.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
