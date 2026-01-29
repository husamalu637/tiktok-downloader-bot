import os
import aiohttp
from aiogram import Bot, Dispatcher, executor, types

# الإعدادات الأساسية
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
        await message.reply("✅ أهلاً بك! البوت عاد للعمل بقوة. أرسل الرابط الآن.")
    else:
        kb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("إشترك هنا 📢", url=CHANNEL_URL))
        await message.reply(f"⚠️ اشترك أولاً في القناة:\n{CHANNEL_ID}", reply_markup=kb)

@dp.message_handler()
async def download(message: types.Message):
    if not await is_sub(message.from_user.id): return await start(message)

    url = message.text
    if "tiktok.com" in url:
        msg = await message.reply("⏳ جاري سحب الفيديو... يرجى الانتظار")
        try:
            # استخدام محرك Loapi - مستقر جداً مع سيرفرات Koyeb
            async with aiohttp.ClientSession() as session:
                api_url = f"https://loapi.com/api/tiktok?url={url}"
                async with session.get(api_url) as r:
                    res = await r.json()
                    # جلب الفيديو بدون علامة مائية
                    video = res.get('video') or res.get('url')
                    if video:
                        await message.answer_video(video, caption="✅ تم التحميل بنجاح!")
                        await msg.delete()
                    else:
                        raise Exception("No video found")
        except:
            # محاولة أخيرة بمحرك طوارئ
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://api.tiklydown.eu.org/api/download?url={url}") as r:
                        res = await r.json()
                        await message.answer_video(res['result']['video']['noWatermark'], caption="✅ تم التحميل (محرك احتياطي)")
                        await msg.delete()
            except:
                await msg.edit_text("❌ الفيديو محمي أو الرابط غير مدعوم حالياً. جرب رابطاً آخر.")
    else:
        await message.reply("⚠️ أرسل رابط تيك توك صحيح.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
