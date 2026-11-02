# pip install aiogram
import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Заполни значения здесь или задай их через переменные окружения
BOT_TOKEN = os.getenv("BOT_TOKEN", "ВСТАВЬ_ТОКЕН_БОТА")
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "your_admin")  # без @

# Меняй этот текст по необходимости.
# Важно: пометка о демо должна оставаться явной.
OFFER_TEXT = """
🎁 ДЕМО-ОФФЕР НА ПОДАРОК

Это демонстрационный пример интерфейса.
Передачи подарка и выплаты звёзд здесь НЕ происходит.

Подарок: {gift_name}
Получатель: {recipient}
"""

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


def offer_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Связаться с администратором",
            url=f"https://t.me/{ADMIN_USERNAME}"
        )]
    ])


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Бот демонстрационных офферов запущен.\n"
        "Используй: /offer <подарок> <получатель>"
    )


@dp.message(Command("offer"))
async def send_demo_offer(message: Message):
    # Пример: /offer Подарок @получатель
    parts = message.text.split(maxsplit=2)
    gift_name = parts[1] if len(parts) > 1 else "не указан"
    recipient = parts[2] if len(parts) > 2 else "не указан"

    text = OFFER_TEXT.format(
        gift_name=gift_name,
        recipient=recipient
    )
    await message.answer(text, reply_markup=offer_keyboard())


@dp.message(Command("id"))
async def show_id(message: Message):
    await message.answer(f"Ваш Telegram ID: {message.from_user.id}")


async def main():
    if BOT_TOKEN == "ВСТАВЬ_ТОКЕН_БОТА":
        raise RuntimeError("Укажи BOT_TOKEN перед запуском")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
