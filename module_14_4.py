from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import logging
from crud_functions import *

api = 'ZZZ'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

products = get_all_products()

kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text='Рассчитать'),
            KeyboardButton(text='Информация')
        ],
        [KeyboardButton(text='Купить')]
    ]
)
inline_buy = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Prodact1', callback_data='product_buying'),
        InlineKeyboardButton(text='Prodact2', callback_data='product_buying'),
        InlineKeyboardButton(text='Prodact3', callback_data='product_buying'),
        InlineKeyboardButton(text='Prodact4', callback_data='product_buying')],
    ]
)


inline_kb = InlineKeyboardMarkup()
inline_butt1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
inline_butt2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
inline_kb.row(inline_butt1, inline_butt2)

logging.basicConfig(
    filename='telegramm_bot.log', filemode='a', encoding='utf-8',
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    level=logging.INFO)
def decor_log(func, message: types.Message, txt):
    async def log_writer(*args, **kwargs):
        try:
            logging.info(f'Получено сообщение от {message.from_user.first_name}: {message["text"]}')
        except KeyError:
            logging.info(f'Получено сообщение от {message.from_user.first_name}: Нажата кнопка - {message["data"]}')
        logging.info(f'Вся информация: {message}')
        rez = await func(*args, **kwargs)
        logging.info(f'Отправлен ответ: {txt}')
        return rez
    return log_writer
class UserState(StatesGroup):
    gender = State()
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands = 'start')
async def start(message):
    txt = 'Мы получили /start.'
    print(txt)
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(f'Привет! \n {message.from_user.username} \n'
                         f' Я Бот помогающий Вашему здоровью. Нажмите на кнопку ', reply_markup=kb)
@dp.message_handler(text='Рассчитать')
async def main_menu(message: types.Message):
    print(f'Сообщение от {message.from_user.first_name}')
    txt = 'Выберите опцию:'
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt, reply_markup=inline_kb)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call: types.CallbackQuery):
    txt = ('Упрощенный вариант формулы Миффлина-Сан Жеора:\n\n'
           'для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5\n'
           'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161\n\n'
           'Формула расчета индекса массы тела (ИМТ):\n\n'
           'ИМТ = вес (кг) / рост (м) ^ 2')
    await call.message.answer(txt)
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_gender(call: types.CallbackQuery):
    txt = 'Введите свой пол (М/Ж):'
    await call.message.answer(txt)
    call.answer = decor_log(call.answer, call, txt)
    await UserState.gender.set()
    await call.answer()

@dp.message_handler(state=UserState.gender)
async def set_age(message, state):
    txt = 'Введите свой возраст:'
    await state.update_data(gender=message.text)
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt)
    await UserState.age.set()
@dp.message_handler(state=UserState.age)
async  def set_growth(message, state):
    await  state.update_data(age= message.text)
    txt = 'Введите свой рост:'
    data = await state.get_data()
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt)
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    txt = 'Введите свой вес:'
    data = await state.get_data()
    await message.answer(txt)
    message.answer = decor_log(message.answer, message, txt)
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await state.finish()
    print(data)


    try:
        if data['gender'].upper() == 'Ж':
            calories = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) - 161
        elif data['gender'].upper() == 'М':
            calories = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5
        else:
            raise ValueError
    except ValueError:
        txt = 'Вы ввели ошибочные данные'
    else:
        txt = f'Ваша норма калорий по формуле Миффлина-Сан Жеора: {calories}'

    message.answer = decor_log(message.answer, message, txt)
    await message.answer(f'Ваша норма калорий по формуле Миффлина-Сан Жеора: {txt}')
    await state.finish()

@dp.message_handler(text='Купить')
async def get_buying_list(message: types.Message):
    for product in products:
        txt = f'{product[1]} | Описание: {product[2]} | Цена: {product[3]} руб.'
        with open(product[4], mode='rb') as img:
            message_answer_log = decor_log(message.answer_photo, message, txt)
            await message_answer_log(img, txt)
    txt = 'Выберите продукт для покупки:'
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt, reply_markup=inline_buy)
@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call: types.CallbackQuery):
    txt = 'Вы успешно приобрели продукт!'
    call.answer = decor_log(call.answer, call, txt)
    await call.message.answer(txt)
    await call.answer()

@dp.message_handler(text='Информация')
async def info(message: types.Message):
    await message.answer('Я -помогу Вам скинуть лишний "жирок"!')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
