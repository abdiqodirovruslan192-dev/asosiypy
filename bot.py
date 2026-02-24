import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.filters import CommandStart
from youtubesearchpython import VideosSearch
import yt_dlp
import os

# Telegram tokeni Shared Variable orqali olinadi
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("🎵 Qo‘shiq nomi yoki video havolasini yuboring!")

@dp.message()
async def handle_message(message: types.Message):
    text = message.text

    if "http" in text:
        await message.answer("⏳ Yuklanmoqda...")
        await download_media(message, text)
    else:
        await message.answer("🔎 Qidirilmoqda...")
        videosSearch = VideosSearch(text, limit=1)
        result = videosSearch.result()
        link = result['result'][0]['link']
        await download_media(message, link)

async def download_media(message, url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'media.%(ext)s'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    await message.answer_video(FSInputFile(filename))
    os.remove(filename)

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
