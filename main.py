import asyncio
import logging

from data.database import database
from aiogram import Bot, Dispatcher
from config.config import load_config, Config
from handlers import user_handlers, other_handlers

logger = logging.getLogger(__name__)
db = database('name_database')


async def main():
    db.create_table()
    logging.basicConfig(level=logging.INFO,
                        format='%(filename)s:%(lineno)d #%(levelname)-8s '
                               '[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot')

    config: Config = load_config()
    bot = Bot(token=config.tg_bot.token,
              parse_mode='HTML')
    dp = Dispatcher()

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())