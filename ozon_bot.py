import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from config.config import load_config
from database.database import start_db
from handlers.base_commands_handlers import base_commands_router
from handlers.realization_report_handler import real_report_router
from handlers.save_headers_handler import shop_data_router

logger = logging.getLogger(__name__)
logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s',
        stream=sys.stdout
)

storage = MemoryStorage()


async def base_commands(bot):
    """Добавление кнопки 'Меню' со списком команд."""
    await bot.set_my_commands(
        [
            BotCommand(
                command='help',
                description='❓ Как пользоваться ботом.'
            ),
            BotCommand(
                command='shop_data',
                description='🔑 Добавить токен и id магазина.'
            ),
            BotCommand(
                command='check_input_data',
                description='📄 Посмотреть введенные данные.'
            ),
        ]
    )


async def main():
    await start_db()
    logger.info('Starting bot')

    config = load_config()
    bot = Bot(
        token=config.tg_bot.token,
        parse_mode=ParseMode.HTML
    )
    dp = Dispatcher(storage=storage)
    dp.include_router(base_commands_router)
    dp.include_router(shop_data_router)
    dp.include_router(real_report_router)
    await base_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Бот принудительно остановлен.')

