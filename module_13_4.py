from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
#from aiogram.dispatcher import FSMContext
#import asyncio

#Задача "Цепочка вопросов":
# Необходимо сделать цепочку обработки состояний для нахождения нормы калорий для человека.

api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())

#    Импортируйте классы State и StatesGroup из aiogram.dispatcher.filters.state.
#     Создайте класс UserState наследованный от StatesGroup.
#     Внутри этого класса опишите 3 объекта класса State: age, growth, weight (возраст, рост, вес).
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands='start')
async def start_message(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.')
# Функцию set_age(message):
#
#     Оберните её в message_handler, который реагирует на текстовое сообщение 'Calories'.
#     Эта функция должна выводить в Telegram-бот сообщение 'Введите свой возраст:'.
#     После ожидать ввода возраста в атрибут UserState.age при помощи метода set.

@dp.message_handler(text = 'Calories')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

    #Функцию set_growth(message, state):
    # Оберните её в message_handler, который реагирует на переданное состояние UserState.age.
    # Эта функция должна обновлять данные в состоянии age на message.text
    #     (написанное пользователем сообщение). Используйте метод update_data.
    # Далее должна выводить в Telegram-бот сообщение 'Введите свой рост:'.
    # После ожидать ввода роста в атрибут UserState.growth при помощи метода set.

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer(f"Введите свой рост:")
    await UserState.growth.set()

# Функцию set_weight(message, state):
#     Оберните её в message_handler, который реагирует на переданное состояние UserState.growth.
#     Эта функция должна обновлять данные в состоянии growth на message.text
#       (написанное пользователем сообщение). Используйте метод update_data.
#     Далее должна выводить в Telegram-бот сообщение 'Введите свой вес:'.
#     После ожидать ввода роста в атрибут UserState.weight при помощи метода set.

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer(f"Введите свой вес:")
    await UserState.weight.set()

#Функцию send_calories(message, state):
    # Оберните её в message_handler, который реагирует на переданное состояние UserState.weight.
    # Эта функция должна обновлять данные в состоянии weight на message.text
    #       (написанное пользователем сообщение). Используйте метод update_data.
    # Далее в функции запомните в переменную data все ранее введённые состояния при помощи state.get_data().
    # Используйте упрощённую формулу Миффлина -
    #       Сан Жеора для подсчёта нормы калорий (для женщин или мужчин - на ваше усмотрение).
    #      BMR=10×массатела (кг)+6,25×рост (см)−5×возраст (годы)+5
    #       Данные для формулы берите из ранее объявленной переменной
    #       data по ключам age, growth и weight соответственно.
    # Результат вычисления по формуле отправьте ответом пользователю в Telegram-бот.
    # Финишируйте машину состояний методом finish().

@dp.message_handler(state = UserState.weight)
async def set_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    bmr = int(data['weight']) * 10 + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f"Ваша норма калорий: {bmr}")
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)