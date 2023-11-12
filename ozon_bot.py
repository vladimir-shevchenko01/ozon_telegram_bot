import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from config.config import Config, load_config
from handlers.base_commands_handlers import base_commands_router
from handlers.save_headers_handler import shop_data_router


logger = logging.getLogger(__name__)


async def base_commands(_bot):
    """Добавление кнопки 'Меню' со списком команд."""
    await _bot.set_my_commands(
        [
            BotCommand(command='help', description='❓ Как пользоваться ботом.'),
            BotCommand(command='shop_data', description='🔑 Добавить токен и id магазина'),
            BotCommand(command='real_data', description='📈 Получить статистику.'),
        ]
    )


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )
    logger.info('Starting bot')

    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token,
              parse_mode='HTML')
    dp = Dispatcher()
    dp.include_router(base_commands_router)
    dp.include_router(shop_data_router)
    await base_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
    
if __name__ == '__main__':
    asyncio.run(main())