
import os
import logging
import requests
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("BOT_TOKEN")
# تأكد من كتابة معرف قناتك هنا بشكل صحيح
CHANNEL_ID = "@YourChannel" 
CHANNEL_URL = f"https://t.me/{CHANNEL_ID.replace('@', '')}"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def is_subscribed(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception:
        return True 

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    check = await is_subscribed(message.from_user.id)
    if check:
        await message.reply("✅ مستعد للعمل! أرسل رابط تيك توك الآن.")
    else:
        keyboard = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("إضغط هنا للإشتراك في القناة 📢", url=CHANNEL_URL)
        keyboard.add(btn)
        await message.reply(f"⚠️ يجب الاشتراك أولاً:\n{CHANNEL_ID}", reply_markup=keyboard)

@dp.message_handler()
async def handle_video(message: types.Message):
    if not await is_subscribed(message.from_user.id):
        await send_welcome(message)
        return
    
    url = message.text
    if "tiktok.com" in url:
        msg = await message.answer("⏳ جاري التحميل... يرجى الانتظار")
        try:
            # استخدام محرك تحميل بديل وأكثر استقراراً
            api_url = f"https://www.tikwm.com/api/?url={url}"
            response = requests.get(api_url).json()
            
            if response.get('code') == 0:
                video_url = "https://www.tikwm.com" + response['data']['play']
                await message.answer_video(video_url, caption="✅ تم التحميل بواسطة بوتك!")
                await msg.delete()
            else:
                await msg.edit_text("❌ فشل الجلب: الرابط قد يكون غير صحيح أو الفيديو خاص.")
        except Exception as e:
            logging.error(f"Error: {e}")
            await msg.edit_text("❌ حدث خطأ فني، حاول مرة أخرى لاحقاً.")
    else:
        await message.reply("⚠️ أرسل رابط تيك توك فقط.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
