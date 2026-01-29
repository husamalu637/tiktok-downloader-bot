import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import TerminatedByOtherGetUpdates

# إعدادات التسجيل
logging.basicConfig(level=logging.INFO)

# --- إعدادات أساسية ---
API_TOKEN = os.getenv("BOT_TOKEN")
# ضع هنا معرف قناتك (يجب أن يبدأ بـ @)
CHANNEL_ID = "@YourChannelUsername" 
# رابط القناة للمستخدمين
CHANNEL_URL = "https://t.me/YourChannelUsername"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# دالة للتحقق من الاشتراك
async def check_subscription(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        # إذا لم يكن العضو مطروداً أو خارج القناة
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    is_subscribed = await check_subscription(message.from_user.id)
    
    if is_subscribed:
        await message.reply("✅ شكراً لاشتراكك! أرسل رابط الفيديو الآن لتحميله.")
    else:
        keyboard = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("اضغط هنا للاشتراك في القناة 📢", url=CHANNEL_URL)
        keyboard.add(btn)
        await message.reply(
            f"⚠️ عذراً! يجب عليك الاشتراك في القناة أولاً لاستخدام البوت.\n\nبعد الاشتراك، أرسل /start مجدداً.",
            reply_markup=keyboard
        )

@dp.message_handler()
async def handle_message(message: types.Message):
    is_subscribed = await check_subscription(message.from_user.id)
    
    if not is_subscribed:
        await send_welcome(message)
        return

    # هنا تضع منطق تحميل الفيديو الخاص بك
    await message.reply("⏳ جاري معالجة الرابط... (تأكد من تحديث منطق التحميل هنا)")

if __name__ == '__main__':
    print("🚀 البوت يعمل الآن بنجاح...")
    # استخدام skip_updates=True لتجاوز رسائل التعارض (Conflict)
    executor.start_polling(dp, skip_updates=True)
