import logging
import sys

from aiogram.types import Message
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import User, ShopKeys

logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s',
        stream=sys.stdout
)

async def db_register_user(message: Message, session: AsyncSession) -> None:

    user = User(telegram_id=int(message.from_user.id))

    session.add(user)

    try:
        await session.commit()
        await session.refresh(user)
        print('Запись создана')
        await session.close()
    except IntegrityError:
        await session.rollback()
        logging.info('Запись уже существует.')



async def db_add_shop_headers(message: Message, session: AsyncSession, token: str | None, shop_id: int | None) -> None:


    token = ShopKeys(user_id=int(message.from_user.id), ozon_admin_token=token, shop_id=shop_id)

    session.add(token)

    try:
        await session.commit()
        await session.refresh(token)
        print('Запись создана')
        await session.close()
    except IntegrityError:
        await session.rollback()
        logging.info('Запись уже существует.')
