from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import sqlite3

db_name = "test.db"
conn = None
curor = None



def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(query):
    cursor.execute(query)
    conn.commit()

def create():
    open()
    do('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username VARCHAR, first_name VARCHAR, last_name VARCHAR, phone_number VARCHAR, password VARCHAR, email VARCHAR)')
    close()


bot = Bot("6264808641:AAGSPtDdf17-bdQ6gVMVnPYHr2NGAkU0qjg")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class UserRegistration(StatesGroup):
    username = State()
    first_name = State()
    last_name = State()
    phone_number = State()
    password = State()
    email = State()

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer("Ласкаво просимо! Для реєстрації, будь ласка, надішліть мені своє ім'я користувача(nickname).")
    await UserRegistration.username.set()

@dp.message_handler(state=UserRegistration.username)
async def process_username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text

    await message.answer("Чудово! Тепер введіть своє ім'я.")
    await UserRegistration.first_name.set()

@dp.message_handler(state=UserRegistration.first_name)
async def process_first_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_name'] = message.text

    await message.answer('Чудово! Тепер введіть своє прізвище.')
    await UserRegistration.last_name.set()


@dp.message_handler(state=UserRegistration.last_name)
async def process_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last_name'] = message.text

    await message.answer('Чудово! Тепер введіть номер телефону.')
    await UserRegistration.phone_number.set()


@dp.message_handler(state=UserRegistration.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text

    await message.answer('Чудово! Тепер придумай свій пароль.')
    await UserRegistration.password.set()

@dp.message_handler(state=UserRegistration.password)
async def process_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text

    await message.answer('Чудово! Тепер введіть свій email.')
    await UserRegistration.email.set()


@dp.message_handler(state=UserRegistration.email)
async def process_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text
        all = (data['username'], data['first_name'], data['last_name'], data['phone_number'], data['password'], data['email'])
        create()
        open()
        cursor.execute('''INSERT INTO users (username, first_name, last_name, phone_number, password, email) VALUES (?,?,?,?,?,?)''', all)
        conn.commit()
        close()
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Site', url = "http://seasonvar.ru/serial-152-Torchvud-1-season.html"))
        await message.reply("Вітаю, ти закінчив реєстрацію, можеш перевірити свій профіль на сайті", reply_markup=markup)
    await state.finish()

executor.start_polling(dp)



