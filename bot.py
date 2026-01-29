
import os
import logging
import requests
from aiogram import Bot, Dispatcher, executor, types

# إعداد السجلات
logging.basicConfig(level=logging.INFO)

# --- الإعدادات (تجلب تلقائياً من Koyeb) ---
API_TOKEN = os.getenv("BOT_TOKEN")

# --- ضع معرف قناتك هنا بدل @YourChannel ---
CHANNEL_ID = "@YourChannel" 
CHANNEL_URL = f"https://t.me/{CHANNEL_ID.replace('@', '')}"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# دالة التحقق من الاشتراك الإجباري
async def is_subscribed(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception:
        # إذا فشل البوت في التحقق (مثلاً ليس مشرفاً)، سيمرر المستخدم لكي لا يتوقف البوت
        return True 

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    check = await is_subscribed(message.from_user.id)
    if check:
        await message.reply("✅ تم التحقق! أنت مشترك. أرسل الآن رابط فيديو تيك توك وسأقوم بتحميله لك.")
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
    # التأكد من الاشتراك أولاً
    if not await is_subscribed(message.from_user.id):
        await send_welcome(message)
        return
    
    url = message.text
    if "tiktok.com" in url:
        msg = await message.answer("⏳ جاري معالجة الرابط وتحميل الفيديو...")
        try:
            # استخدام API خارجي مجاني لتحميل الفيديو بدون علامة مائية
            api_url = f"https://api.tiklydown.eu.org/api/download?url={url}"
            response = requests.get(api_url).json()
            video_url = response['result']['video']['noWatermark']
            
            await message.answer_video(video_url, caption="✅ تم التحميل بنجاح!")
            await msg.delete()
        except Exception as e:
            logging.error(f"Error: {e}")
            await message.reply("❌ عذراً، فشل تحميل الفيديو. تأكد من أن الحساب عام وليس خاصاً.")
    else:
        await message.reply("⚠️ من فضلك أرسل رابط تيك توك صحيح.")

if __name__ == '__main__':
    # skip_updates=True تحل مشكلة التعارض Conflict التي تظهر في سجلاتك
    executor.start_polling(dp, skip_updates=True)
