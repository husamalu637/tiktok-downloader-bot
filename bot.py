
@dp.message_handler()
async def handle_video(message: types.Message):
    if not await is_subscribed(message.from_user.id):
        await send_welcome(message)
        return
    
    url = message.text
    if "tiktok.com" in url:
        await message.answer("⏳ جاري استخراج الفيديو من تيك توك...")
        try:
            # هنا نستخدم API خارجي مجاني لكي لا يستهلك البوت مساحة السيرفر
            import requests
            api_url = f"https://api.tiklydown.eu.org/api/download?url={url}"
            response = requests.get(api_url).json()
            video_url = response['result']['video']['noWatermark']
            
            await message.answer_video(video_url, caption="✅ تم التحميل بنجاح بواسطة بوتك!")
        except Exception as e:
            await message.reply("❌ عذراً، حدث خطأ أثناء جلب الفيديو. تأكد من الرابط.")
    else:
        await message.reply("⚠️ من فضلك أرسل رابط تيك توك صحيح.")

