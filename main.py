import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import aiohttp

API_TOKEN = '8430773840:AAER2cQ3CbMgNGQuGcBvpb2mwyziLA6_kj0'
CHANNEL_USERNAME = '@NexusXScripts'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

scripts = {
    "Blox Fruits": {
        "name": "Redz Hub",
        "code": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/tlredz/Scripts/refs/heads/main/main.luau"))()'
    },
    "Realistic Street Soccer": {
        "name": "Verbal Hub",
        "code": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/VerbalHubz/Verbal-Hub/refs/heads/main/Realistic%20Street%20Soccer%20Op%20Script",true))()'
    },
    "Ink Game": {
        "name": "Tora IsMe",
        "code": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/gumanba/Scripts/main/InkGame"))()'
    }
}

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    try:
        user = await bot.get_chat_member(CHANNEL_USERNAME, message.from_user.id)
        if user.status in ['member', 'creator', 'administrator']:
            kb = InlineKeyboardMarkup(row_width=1)
            for game in scripts:
                kb.add(InlineKeyboardButton(text=game, callback_data=game))
            await message.answer("Выберите игру, чтобы получить скрипт:", reply_markup=kb)
        else:
            await message.answer(f"Чтобы пользоваться ботом, подпишитесь на канал {CHANNEL_USERNAME}")
    except:
        await message.answer(f"Чтобы пользоваться ботом, подпишитесь на канал {CHANNEL_USERNAME}")

@dp.callback_query_handler(lambda c: c.data in scripts)
async def send_script(callback_query: types.CallbackQuery):
    game = callback_query.data
    script = scripts[game]
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        f"📋 Скрипт: {script['name']}\n\n📄 Код скрипта:\n`{script['code']}`",
        parse_mode='Markdown'
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)