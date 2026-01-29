import os
import logging
from aiogram import Bot, Dispatcher, executor, types

# إعداد السجلات
logging.basicConfig(level=logging.INFO)

# --- الإعدادات ---
API_TOKEN = os.getenv("BOT_TOKEN")

# استبدل الكلمة بالأسفل بمعرف قناتك (مثال: @MyChannel)
CHANNEL_ID = "@اكتب_معرف_قناتك_هنا" 
CHANNEL_URL = f"https://t.me/{CHANNEL_ID.replace('@', '')}"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# دالة التحقق من الاشتراك
async def is_subscribed(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logging.error(f"خطأ في التحقق: {e}")
        # إذا لم يكن البوت مشرفاً، سيعتبر الجميع مشتركين لكي لا يتوقف العمل
        return True 

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    check = await is_subscribed(message.from_user.id)
    if check:
        await message.reply("✅ تم التحقق! أنت مشترك بالفعل. أرسل الرابط الآن.")
    else:
        keyboard = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("إضغط هنا للإشتراك 📢", url=CHANNEL_URL)
        keyboard.add(btn)
        await message.reply(
            f"⚠️ عذراً، يجب عليك الاشتراك في القناة أولاً لاستخدام البوت:\n{CHANNEL_ID}",
            reply_markup=keyboard
        )

@dp.message_handler()
async def handle_video(message: types.Message):
    if not await is_subscribed(message.from_user.id):
        await send_welcome(message)
        return
    
    # هنا يتم استلام الرابط
    await message.answer("⏳ جاري التحميل... يرجى الانتظار.")

if __name__ == '__main__':
    # حل مشكلة التعارض (Conflict) التي تظهر في سجلاتك
    executor.start_polling(dp, skip_updates=True)
