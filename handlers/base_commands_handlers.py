from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import StateFilter, CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.utils import markdown
from LEXICON.ru_lexicon import base_info_message
from database.database import users

base_commands_router = Router()


@base_commands_router.message(CommandStart(), StateFilter(default_state))
async def command_start_handler(message: Message) -> None:
    """Команда start."""

    await message.answer(base_info_message['start'].format('@' + message.from_user.full_name))
    user = message.from_user.id
    if user not in users:
        users.append(message.from_user.id)


