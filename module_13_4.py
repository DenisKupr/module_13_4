from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup()
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button)
kb.add(button2)
#kb.row kb.insert


class UserState(StatesGroup):
    age = State()   # Состояние для возраста
    growth = State()   # Состояние для роста
    weight = State()   # Состояние для веса

@dp.message_handler(commands=['start'])
async def start_message(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Рассчитать', 'Информация']
    keyboard.add(*buttons)
    await message.answer("Привет! я бот помогающий твоему здоровью.", reply_markup=keyboard)


# Хэндлер начального вызова
@dp.message_handler(text=["Рассчитать"])
async def set_age(message: types.Message):
    await message.reply("Введите свой возраст:")
    await UserState.age.set()

# Хэндлер для возраста
@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

# Хэндлер для роста
@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

# Хэндлер для веса и подсчета калорий
@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()


    age = int(data.get('age'))
    growth = int(data.get('growth'))
    weight = int(data.get('weight'))

    # Упрощенная формула Миффлина - Сан Жеора для мужчин
    bmr = 10 * weight + 6.25 * growth - 5 * age + 5
    await message.answer(f'Ваша норма калорий: {bmr}')

    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
