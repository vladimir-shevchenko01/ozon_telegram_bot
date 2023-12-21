from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_commands import db_register_user, db_add_shop_headers

from bot_states.states import FSMShopHeaders
from database.database import ShopKeys, User, database, engine

shop_data_router = Router()


@shop_data_router.message(Command(commands='shop_data'), StateFilter(default_state))
async def get_shop_data_command(message: Message, state: FSMContext):
    await message.answer(text='Введите Seller ID')
    await state.set_state(FSMShopHeaders.shop_id)


@shop_data_router.message(StateFilter(FSMShopHeaders.shop_id), F.text.isdigit())
async def get_shop_id_command(message: Message, state: FSMContext):
    await state.update_data(client_id=message.text)
    await message.answer(text='Теперь введите API KEY администратора')
    await state.set_state(FSMShopHeaders.api_key)


@shop_data_router.message(StateFilter(FSMShopHeaders.shop_id))
async def non_correct_shop_id(message: Message):
    await message.answer(
        text='Проверьте корректность введенных данных.'
    )


@shop_data_router.message(StateFilter(FSMShopHeaders.api_key))
async def get_api_key(message: Message, state: FSMContext):
    await state.update_data(api_key=message.text)

    # Сохраняем пользователя и введенные данные
    # в базу данных
    user = message.from_user.id
    data = await state.get_data()
    database[user] = data
    session = AsyncSession(engine)
    await db_add_shop_headers(message=message, session=session, token=data['api_key'], shop_id=data['client_id'])
    # Создаем клавиатуру.
    get_shop_data_button = InlineKeyboardButton(
        text='Месячный отчет о реализации 💰',
        callback_data='real_rep'
    )
    cancel_data_button = InlineKeyboardButton(
        text='Отменить введенные данные ❌',
        callback_data='cancel'
    )
    keyboard: list[list[InlineKeyboardButton]] = [
        [get_shop_data_button],
        [cancel_data_button],
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    # Выводим клавиатуру.
    await message.answer(
        text='Отлично!\n\n'
             'Теперь Вы перейти к получению отчета '
             'или сбросить введенные данные.',
        reply_markup=markup
    )
