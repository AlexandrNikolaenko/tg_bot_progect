import re
from aiogram import Router
from aiogram import F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from data.db import User
import asyncio

# Функционал для добавления пользователей и данных о их финансовом состоянии
pull_data = Router()
start_proc = Router()


class WaitingState(StatesGroup):
    WAIT = State()
    WAIT_STATS = State()
    NOT_WAIT = State()
    ADD_INFO = State()


LAST_MESSAGE = dict()
UPDATE_STATS = dict()


# Начало взаимодействия с ботом
@start_proc.message(Command('start'))
async def handle_start(message: Message):
    await message.reply('Choice the command:\n/start - show commands\n/add_data - add information about Your finance '
                        'condition\n/recommendation - to see recommendations\n/my_rate - to see Your rating')


# Добавление доходов в бд
@pull_data.message(WaitingState.WAIT_STATS, F.text.regexp(r'gain: \d{3,}'))
async def new_gain(message: Message):
    for is_user in User.select():
        if is_user.id_ == message.from_user.id:
            text = str(message.text)
            if is_user.gain is not None:
                is_user.gain += '\n' + text[6::]
            else:
                is_user.gain = text[6::]
            UPDATE_STATS[f'{message.from_user.id}']['gain'] = True
            is_user.save()
            await message.reply(f'Gain was added\nYour gain:\n{is_user.gain}')
            break


# Добавление расходов в бд
@pull_data.message(WaitingState.WAIT_STATS, F.text.regexp(r'cost: \d{3,}'))
async def new_cost(message: Message):
    for is_user in User.select():
        if is_user.id_ == message.from_user.id:
            text = str(message.text)
            if is_user.cost is not None:
                is_user.cost += '\n' + text[6::]
            else:
                is_user.cost = text[6::]
            UPDATE_STATS[f'{message.from_user.id}']['cost'] = True
            is_user.save()
            await message.reply(f'Cost was added\nYour cost:\n{is_user.cost}')
            break


@pull_data.message(WaitingState.ADD_INFO, F.text.regexp(r'[^/_]'))
async def add_info(message: Message):
    LAST_MESSAGE[f'{message.from_user.id}'] = str(message.text)


@pull_data.message(Command('add_data'))
async def handle_pull(message: Message, state: FSMContext):
    await state.set_state(WaitingState.WAIT)
    user = message.from_user
    LAST_MESSAGE[f'{user.id}'] = str(message.text)
    UPDATE_STATS[f'{user.id}'] = {'gain': False, 'cost': False}
    for stroke in User.select():
        if stroke.id_ != user.id:
            continue
        else:
            if not (stroke.finance is None):
                await message.reply('Add new information')
                await state.set_state(WaitingState.ADD_INFO)
                while re.search('[/_]', LAST_MESSAGE[f'{user.id}']) is not None:
                    await asyncio.sleep(0.2)
                new_info = LAST_MESSAGE[f'{user.id}']
                stroke.finance += '\n' + new_info
                stroke.save()
            else:
                await message.reply("There aren't information about You, please add it")
                await state.set_state(WaitingState.ADD_INFO)
                while re.search('[/_]', LAST_MESSAGE[f'{user.id}']) is not None:
                    await asyncio.sleep(0.2)
                new_info = LAST_MESSAGE[f'{user.id}']
                stroke.finance = new_info
                stroke.save()
            await state.set_state(WaitingState.WAIT_STATS)
            await message.reply('Put Your gain and cost as:\ncost: sum\ngain: sum')
            break
    while not UPDATE_STATS[f'{user.id}']['gain'] or not UPDATE_STATS[f'{user.id}']['cost']:
        await asyncio.sleep(0.2)
    await state.set_state(WaitingState.NOT_WAIT)
    await message.reply('Information was added')

