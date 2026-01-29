import logging
from aiogram import Bot, Dispatcher, types, executor

# إعدادات البوت
TOKEN = "7629555198:AAHtDq7N7P6t0uW8_8O5zW9S5V3TzX8V9U0"
CHANNEL = "@husam22227"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    try:
        user = await bot.get_chat_member(chat_id=CHANNEL, user_id=message.from_user.id)
        if user.status in ['member', 'administrator', 'creator']:
            await message.answer("✅ أهلاً بك! أنت مشترك في القناة ويمكنك استخدام البوت.")
        else:
            await message.answer(f"⚠️ يرجى الاشتراك في القناة أولاً:\nhttps://t.me/husam22227")
    except:
        await message.answer("⚠️ تأكد من رفع البوت مسؤولاً في القناة.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

