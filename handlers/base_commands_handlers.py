from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from aiogram.utils import markdown

from database.database import users
from LEXICON.ru_lexicon import base_info_message

base_commands_router = Router()


@base_commands_router.message(CommandStart(), StateFilter(default_state))
async def command_start_handler(message: Message) -> None:
    """Команда start."""

    await message.answer(base_info_message['start'].format('@' + message.from_user.full_name))
    user = message.from_user.id
    if user not in users:
        users.append(message.from_user.id)


@base_commands_router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы введенные данные\n\n'
             'Чтобы снова перейти к заполнению данных магазина '
             'отправьте команду /shop_data'
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()



