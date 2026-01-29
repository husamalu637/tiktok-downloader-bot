import os
import logging
from aiogram import Bot, Dispatcher, executor, types

# إعداد السجلات (بأقل استهلاك للطاقة)
logging.basicConfig(level=logging.INFO)

# جلب التوكن من إعدادات السيرفر
API_TOKEN = os.getenv("BOT_TOKEN")

# التحقق من وجود التوكن
if not API_TOKEN:
    print("خطأ: لم يتم العثور على BOT_TOKEN!")
    exit()

# تشغيل البوت والموزع
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("أهلاً بك! البوت يعمل الآن بأقل استهلاك للذاكرة 🚀")

if __name__ == '__main__':
    print("جاري بدء تشغيل البوت...")
    executor.start_polling(dp, skip_updates=True)
