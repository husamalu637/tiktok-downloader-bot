import os
import logging
import aiohttp
from aiogram import Bot, Dispatcher, executor, types

# إعداد السجلات لمراقبة أداء البوت
logging.basicConfig(level=logging.INFO)

# جلب التوكن تلقائياً من إعدادات Koyeb
API_TOKEN = os.getenv("BOT_TOKEN")

# --- تم إضافة معرف قناتك هنا بنجاح ---
CHANNEL_ID = "@husam22227" 
CHANNEL_URL = "https://t.me/husam22227"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# دالة للتحقق من أن المستخدم مشترك في قناتك
async def is_subscribed(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logging.error(f"خطأ في التحقق من الاشتراك: {e}")
        # في حال حدوث خطأ فني، سيسمح للبوت بالعمل لضمان عدم توقفه
        return True 

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    check = await is_subscribed(message.from_user.id)
    if check:
        await message.reply("✅ تم التحقق من اشتراكك بنجاح! أرسل الآن رابط فيديو تيك توك لتحميله.")
    else:
        keyboard = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("إضغط هنا للإشتراك في القناة 📢", url=CHANNEL_URL)
        keyboard.add(btn)
        await message.reply(
            f"⚠️ عذراً، يجب عليك الاشتراك في القناة أولاً لاستخدام البوت:\n{CHANNEL_ID}",
            reply_markup=keyboard
        )

@dp.message_handler()
async def handle_video(message: types.Message):
    # التحقق من الاشتراك قبل البدء بالتحميل
    if not await is_subscribed(message.from_user.id):
        await send_welcome(message)
        return
    
    url = message.text
    if "tiktok.com" in url:
        msg = await message.answer("⏳ جاري جلب الفيديو... يرجى الانتظار")
        try:
            async with aiohttp.ClientSession() as session:
                # استخدام محرك تحميل سريع ومستقر
                api_url = f"https://www.tikwm.com/api/?url={url}"
                async with session.get(api_url) as resp:
                    data = await resp.json()
                    if data.get('code') == 0:
                        video_url = "https://www.tikwm.com" + data['data']['play']
                        await message.answer_video(video_url, caption="✅ تم التحميل بنجاح بواسطة بوتك!")
                        await msg.delete()
                    else:
                        await msg.edit_text("❌ فشل الجلب: قد يكون الفيديو خاصاً أو الرابط غير صحيح.")
        except Exception as e:
            logging.error(f"خطأ في التحميل: {e}")
            await msg.edit_text("❌ حدث خطأ فني مؤقت، يرجى المحاولة مرة أخرى لاحقاً.")
    else:
        await message.reply("⚠️ من فضلك أرسل رابط تيك توك صحيح.")

if __name__ == '__main__':
    # skip_updates=True لحل مشكلة التعارض (Conflict) الظاهرة في سجلاتك
    executor.start_polling(dp, skip_updates=True)
