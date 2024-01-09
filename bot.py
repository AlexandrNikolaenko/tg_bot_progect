import tomllib
import aiogram as ag
from aiogram.dispatcher.dispatcher import Dispatcher
from routers.rec import rec_router
from routers.per_rate import per_rate_router
from routers.pull_data import pull_data, start_proc
from middlewares.users import UsersMiddlewares
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout
)

with open('config.toml', 'rb') as cfg:
    config = tomllib.load(cfg)

bot = ag.Bot(config['telegram']['token'])
dispatcher = Dispatcher()

dispatcher.message.middleware(UsersMiddlewares())
dispatcher.include_router(start_proc)
dispatcher.include_router(rec_router)
dispatcher.include_router(per_rate_router)
dispatcher.include_router(pull_data)

dispatcher.run_polling(bot)
