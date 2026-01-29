import os
import logging
from aiogram import Bot, Dispatcher, executor, types

# إعداد السجلات (Logs)
logging.basicConfig(level=logging.INFO)

# جلب التوكن من إعدادات البيئة (أمان عالي)
API_TOKEN = os.getenv("BOT_TOKEN")

# التحقق من وجود التوكن
if not API_TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables!")

# إنشاء البوت والموزع
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    هذا المعالج يستجيب لأوامر /start و /help
    """
    await message.reply("أهلاً بك! أنا بوت تحميل تيك توك.\nأرسل لي رابط الفيديو وسأقوم بتحميله لك.")

@dp.message_handler()
async def echo(message: types.Message):
    # هنا سنضيف لاحقاً منطق التحميل، حالياً سيقوم البوت برد الرسالة
    await message.answer(f"لقد استلمت الرابط: {message.text}\nجاري العمل على معالجته...")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
