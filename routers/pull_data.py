import time
import re
from aiogram import Router
from aiogram import F
from aiogram import types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from data.db import User, FINANCES

# Функционал для добавления пользователей и данных о их финансовом состоянии
pull_data = Router()
start_proc = Router()


class WaitingState(StatesGroup):
    WAIT = State()
    WAIT_STATS = State()
    NOT_WAIT = State()
    ADD_INFO = State()


# Начало взаимодействия с ботом
@start_proc.message(Command('start'))
async def handle_start(message: Message):
    await message.reply('Choice the command:\n/start - show commands\n/add_data - add information about Your finance '
                        'condition\n/recommendation - to see recommendations\n/my_rate - to see Your rating')


# Добавление статистических данных
@pull_data.message(WaitingState.WAIT_STATS, F.text.regexp(r'cost: \d{3,}'))
async def new_gain(message: Message):
    while True:
        if str(message.text) == r'cost: \d{3,}':
            try:
                text = message.text[6::]
                return int(text)
            except ValueError:
                await message.reply('Please put by numbers')
                return await new_gain(message)
        else:
            time.sleep(0.2)


@pull_data.message(WaitingState.WAIT_STATS, F.text.regexp(r'gain: \d{3,}'))
async def new_cost(message: Message):
    while True:
        if message.etxt == r'gain: \d{3,}':
            try:
                text = message.text[6::]
                return int(text)
            except ValueError:
                await message.reply('Please put by numbers')
                return await new_cost(message)
        else:
            time.sleep(0.2)


@pull_data.message(WaitingState.ADD_INFO)
async def add_info(message: Message):
    while True:
        if re.search('[/_]', str(message.text)) is None:
            return str(message.text)
        else:
            time.sleep(0.2)
            print('asd', message.text)


@pull_data.message(WaitingState.WAIT_STATS)
async def push_to_finance(id_user, message: Message):
    count = 0
    find = False
    for is_user in FINANCES:
        if is_user == id_user:
            FINANCES[count]['gain'].append(await new_gain(message))
            FINANCES[count]['cost'].append(await new_cost(message))
            find = True
            break
        count += 1
    if not find:
        FINANCES.append({'user_id': id_user, 'gain': await new_gain(), 'cost': await new_cost()})


@pull_data.message(Command('add_data'))
async def handle_pull(message: Message, state: FSMContext):
    user = message.from_user
    for stroke in User.select():
        if stroke.id_ != user.id:
            continue
        else:
            if not (stroke.finance is None):
                await message.reply('Add new information')
                await state.set_state(WaitingState.ADD_INFO)
                new_info = str(await add_info(message))
                stroke.finance += '/n' + new_info
                stroke.save()
            else:
                await message.reply("There aren't information about You, please add it")
                await state.set_state(WaitingState.ADD_INFO)
                new_info = str(await add_info(message))
                stroke.finance = new_info
                stroke.save()
            await state.set_state(WaitingState.WAIT_STATS)
            await push_to_finance(user.id, message)
            await state.set_state(WaitingState.NOT_WAIT)
            await message.reply('Information was added')
            break
