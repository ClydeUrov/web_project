import logging
import os
import re
import aiohttp
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from bs4 import BeautifulSoup
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
async def send_on_site(message: types.Message, state: FSMContext):
    # Отримуємо CSRF токен
    await message.answer("Вас вітає наша телеграм реєстрація!\nДля початку Введи своє ім'я")
    await Form.name.set()

    async with state.proxy() as data:
        print(data)
    url = 'http://127.0.0.1:8000/'
    # встановіть URL вашого ендпоінту
    print(message)
    async with aiohttp.ClientSession() as session:
        async with session.post('http://127.0.0.1:8000/', data={"message": message.text}) as resp:
            print(111, resp.status)
        async with session.get('http://127.0.0.1:8000/') as response:
            csrf_token = response.cookies['csrftoken']
            print(csrf_token)
            headers = {'X-CSRFToken': str(csrf_token)}
            async with session.post(url, data={"message": message.text}, headers=headers) as resp:
                print(resp)
                data = {"message": message.text, "username": message.from_user.username,
                        "user_id": message.from_user.id,
                        "first_name": message.from_user.first_name, "last_name": message.from_user.last_name,
                        "name": "Dima", 'email': "G@gmail.com", 'password': "qwert"}
            async with session.post(url, data=data, headers=headers) as resp:
                print(resp.status)
                # print(await resp.text())
    await state.finish()



    # url = 'http://127.0.0.1:8000/'
    # async with aiohttp.ClientSession() as session:
    #     async with session.get('http://127.0.0.1:8000/') as response:
    #         html = await response.text()
    #         soup = BeautifulSoup(html, 'html.parser')
    #         csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    #         print(csrf_token)
    #         csrf_token = response.cookies['csrftoken']
    #         print(csrf_token)
    #         headers = {'X-CSRFToken': str(csrf_token)}
    #         data = {'key': 'value'}
    #         async with session.post(url, data=data, headers=headers) as resp:
    #             response_text = await resp.text()
    #         html = await response.text()
    #         soup = BeautifulSoup(html, 'html.parser')
    #         csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    #         print(csrf_token)
    #         # csrf_token = response.cookies['csrfmidlewaretoken']
    #         # print(csrf_token)
    #         headers = {'X-CSRFToken': str(csrf_token)}
    #         data = {"message": message.text, "username": message.from_user.username, "user_id": message.from_user.id,
    #                 "first_name": message.from_user.first_name, "last_name": message.from_user.last_name,
    #                 "name": 'Dima', 'email': 'D@gmail.com', 'password': '12345'}
    #         async with session.post(url, data=data, headers=headers) as resp:
    #             print(await resp.text())


    # url = 'http://127.0.0.1:8000/servants/login/'
    # login_page_url = 'http://127.0.0.1:8000/servants/login/'
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(login_page_url) as login_page:
    #         csrf_token = login_page.cookies['csrftoken']
    #         # print(csrf_token)
    #         # csrf_token = login_page.cookies.get('csrftoken').value
    #         # print(csrf_token)
    #
    #         data = {'name': message.text}
    #         headers = {'X-CSRFToken': str(csrf_token)}
    #         print(headers)
    #     async with session.post(url, data=data, headers={'X-CSRFToken': str(csrf_token)}) as resp:
    #         print()
    #         response_text = await resp.text()

    # async with aiohttp.ClientSession() as session:
    #     # отправляем GET-запрос для получения CSRF-токена
    #     async with session.get(url) as resp:
    #         soup = BeautifulSoup(await resp.text(), 'html.parser')
    #         csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'}).get('value')
    #         print(csrf_token)
    #     # отправляем POST-запрос с токеном в заголовке
    #     data = {'name': message.text}
    #     headers = {'X-CSRFToken': str(csrf_token)}
    #     async with session.post(url, data=data, headers=headers) as resp:
    #         print(await resp.text())


    # async with aiohttp.ClientSession() as session:
    #     # отправляем GET-запрос для получения CSRF-токена
    #     async with session.get(url) as resp:
    #         csrf_token = resp.cookies.get('csrftoken').value
    #
    #     # отправляем POST-запрос с токеном в заголовке
    #     data = {'name': message.text}
    #     headers = {'X-CSRFToken': csrf_token}
    #     async with session.post(url, data=data, headers=headers) as resp:
    #         print(await resp.text())
    # async with aiohttp.ClientSession() as session:
    #     async with session.get("http://127.0.0.1:8000/") as resp:
    #         csrf_token = resp.cookies['csrftoken']
    #         headers = {'X-CSRFToken': str(csrf_token)}
    #         if csrf_token:
    #             data = {"message": message.text, "username": message.from_user.username,
    #                     "user_id": message.from_user.id,
    #                     "first_name": message.from_user.first_name, "last_name": message.from_user.last_name,
    #                     "name": 'Dima', 'email': 'D@gmail.com', 'password': '12345'}
    #             # headers = {'X-CSRFToken': str(csrf_token.value)}
    #             async with session.post(url, data=data, headers=headers) as resp:
    #                 print(resp.cookies)
    #                 print(await resp.text())
        # async with session.get('http://127.0.0.1:8000') as response:
        #     csrf_token = response.cookies['csrftoken']
        #     print(csrf_token)

    # user = message.from_user
    # profile_photos = await user.get_profile_photos()
    # print(profile_photos)
    # file = await profile_photos.photos[0].get_file()
    # file_path = "photos/123.jpg"
    # with open(file_path, 'wb') as f:
    #     f.write(file.getbuffer())
    # user = message.from_user
    #
    # # Отримуємо список фотографій користувача
    # profile_photos = await user.get_profile_photos()
    #
    # # Ітеруємося по списку фотографій та зберігаємо їх
    # for index, photo in enumerate(profile_photos.photos, start=1):
    #     # Завантажуємо фото
    #     file = await bot.download_file_by_id(photo[-1].file_id)
    #     print(file)
    #     # Створюємо папку photos, якщо вона ще не існує
    #     if not os.path.exists('photos'):
    #         os.mkdir('photos')
    #
    #     # Зберігаємо фото у файл
    #     file_path = f"photos/123.jpg"
    #     print(file_path)
    #     with open(file_path, 'wb') as f:
    #         f.write(file.getbuffer())


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

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
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
    url = 'http://127.0.0.1:8000//servants/login'
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:8000') as response:
            csrf_token = response.cookies['csrftoken']
            print(csrf_token)
            headers = {'X-CSRFToken': str(csrf_token)}
            data = {"message": message.text, "username": message.from_user.username, "user_id": message.from_user.id,
                    "first_name": message.from_user.first_name, "last_name": message.from_user.last_name,
                    "name": data['name'], 'email': data['email'], 'password': data['password']}
            async with session.post(url, data=data, headers=headers) as resp:
                print(resp.status)
                print(await resp.text())
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
