import logging
import os
import re
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import requests
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()
BOT_TOKEN = os.environ["TG_TOKEN"]
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    name = State()
    email = State()
    password = State()


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Вас вітає наша телеграм реєстрація!\nДля початку Введи своє ім'я")
    await Form.name.set()


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text

    await message.answer("Введіть свій E-mail")
    await Form.next()


@dp.message_handler(state=Form.email)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["email"] = message.text

    await message.answer("Введіть свій пароль.")
    await Form.next()


@dp.message_handler(state=Form.password)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["password"] = message.text

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton("Підтвердити"))
        keyboard.add(KeyboardButton("Скасувати та ввести знову"))
        await message.answer(
            f"Введені данні:\nІм'я: {data['name']}\nE-mail: {data['email']}\nПароль: {data['password']}",
            parse_mode=ParseMode.HTML, reply_markup=keyboard
        )

        await Form.next()


@dp.message_handler(regexp=re.compile(r"Скасувати та ввести знову", re.IGNORECASE))
async def cancel_registration(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer("Ваша реєстрація була скасована. Введіть своє ім'я ще раз, щоб почати реєстрацію.")
    await Form.name.set()


@dp.message_handler(regexp=re.compile(r"Підтвердити", re.IGNORECASE))
async def send_on_site(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        print(data)
    url = 'http://127.0.0.1:8000/'
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/') as response:
            csrf_token = response.cookies['csrftoken']
            headers = {'X-CSRFToken': str(csrf_token)}
            data = {"message": message.text, "username": message.from_user.username, "user_id": message.from_user.id,
                    "first_name": message.from_user.first_name, "last_name": message.from_user.last_name,
                    "name": data['name'], 'email': data['email'], 'password': data['password']}
            async with session.post(url, data=data, headers=headers) as resp:
                print(await resp.text())
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
