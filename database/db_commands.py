from aiogram.types import Message
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
import logging
import sys

from database.database import User

logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s',
        stream=sys.stdout
)

async def db_register_user(message: Message, session: AsyncSession):

    user = User(telegram_id=int(message.from_user.id))

    session.add(user)

    try:
        await session.commit()
        await session.refresh(user)
        print('Запись создана')
        await session.close()
        return True
    except IntegrityError:
        await session.rollback()
        logging.info('Запись уже существует.')
        return False