import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# إعدادات البوت والقناة
TOKEN = '7629555198:AAHtDq7N7P6t0uW8_8O5zW9S5V3TzX8V9U0'
CHANNEL_ID = '@husam22227'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    try:
        user_status = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)
        if user_status.status in ['member', 'administrator', 'creator']:
            await message.answer("✅ أهلاً بك! أنت مشترك في القناة ويمكنك استخدام البوت.")
        else:
            await message.answer(f"⚠️ عذراً! يجب عليك الاشتراك في القناة أولاً:\nhttps://t.me/husam22227")
    except Exception as e:
        await message.answer("تأكد من وجود البوت كمسؤول في القناة.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

