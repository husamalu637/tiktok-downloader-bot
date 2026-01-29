import os
import logging
import yt_dlp
import aiohttp
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

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
        await message.reply("✅ البوت جاهز للعمل بأحدث التقنيات! أرسل الرابط.")
    else:
        kb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("إشترك هنا 📢", url=CHANNEL_URL))
        await message.reply(f"⚠️ اشترك أولاً:\n{CHANNEL_ID}", reply_markup=kb)

@dp.message_handler()
async def download_video(message: types.Message):
    if not await is_sub(message.from_user.id): return await start(message)

    url = message.text
    if "tiktok.com" in url:
        msg = await message.reply("⏳ جاري كسر التشفير وتحميل الفيديو...")
        
        # المحاولة الأولى: باستخدام مكتبة yt-dlp مع هوية مزيفة
        try:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'quiet': True,
                'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                video_url = info.get('url')
                if video_url:
                    await message.answer_video(video_url, caption="✅ تم التحميل (محرك داخلي)")
                    await msg.delete()
                    return
        except:
            pass # إذا فشلت المكتبة، ننتقل للمحرك الثاني تلقائياً

        # المحاولة الثانية: استخدام API خارجي سريع (كخطة بديلة)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://www.tikwm.com/api/?url={url}") as r:
                    res = await r.json()
                    video = "https://www.tikwm.com" + res['data']['play']
                    await message.answer_video(video, caption="✅ تم التحميل (محرك احتياطي)")
                    await msg.delete()
        except:
            await msg.edit_text("❌ عذراً، تيك توك يمنع هذا الرابط حالياً. جرب رابطاً آخر.")
    else:
        await message.reply("⚠️ أرسل رابط تيك توك صحيح.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
