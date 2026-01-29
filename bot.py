import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = '7629555198:AAHtDq7N7P6t0uW8_8O5zW9S5V3TzX8V9U0'
CHANNEL_ID = '@husam22227'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user = await bot.get_chat_member(CHANNEL_ID, message.from_user.id)
    if user.status not in ['member', 'administrator', 'creator']:
        await message.answer(f"يجب الاشتراك في القناة أولاً: {CHANNEL_ID}")
    else:
        await message.answer("أهلاً بك! أنت مشترك بالفعل.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
