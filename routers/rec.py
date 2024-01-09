from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from data.db import User

# Этот функционал должен будет общаться с ChatGPT или испоьльзовать его API и
# получать рекомендации для улучшения финансовой ситуации

rec_router = Router()


class RecStates(StatesGroup):
    pass


