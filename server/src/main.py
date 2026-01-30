import os
import logging
import asyncio
from pathlib import Path
from aiogram import Bot,Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
from pathlib import Path
logging.basicConfig(level=logging.INFO)




BASE_DIR = Path(__file__).resolve().parent.parent.parent
dotenv_path = BASE_DIR / "api.env"

load_dotenv(dotenv_path=dotenv_path)

token = os.getenv("TOKEN")
if not token:
    raise ValueError(f"Токен не найден! Проверьте файл: {dotenv_path}")

bot = Bot(token=token)




dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message : types.Message):
    await message.answer("отправь сообщение прям мне и я опубликую его в группе")

@dp.message()
async def handle_message(message: types.Message):
    target_id = os.getenv("id")
    

    if not target_id:
        await message.answer("Ошибка: ID получателя не настроен.")
        return

    try:

        await message.copy_to(chat_id=target_id)
        await message.answer("Сообщение доставлено!")
    except Exception as e:

        logging.error(f"Ошибка отправки: {e}")
        await message.answer(f"Не удалось отправить. Ошибка: {e}")


async def main():
    await dp.start_polling(bot)

if __name__ in "__main__":
    asyncio.run(main())