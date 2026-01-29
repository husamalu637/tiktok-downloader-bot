import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# إعدادات البوت والقناة
TOKEN = '7629555198:AAHtDq7N7P6t0uW8_8O5zW9S5V3TzX8V9U0' # توكن البوت الخاص بك
CHANNEL_ID = '@husam22227' # معرف قناتك

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

async def is_subscribed(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("مرحباً بك في بوت تحميل فيديوهات تيك توك!")

@dp.message_handler()
async def check_and_download(message: types.Message):
    if not await is_subscribed(message.from_user.id):
        await message.answer(f"⚠️ عذراً! يجب عليك الاشتراك في القناة أولاً لتتمكن من استخدام البوت:\n{CHANNEL_ID}")
        return
    
    # هنا يتم وضع كود التحميل الفعلي
    await message.answer("✅ أنت مشترك! جاري معالجة الرابط...")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    
