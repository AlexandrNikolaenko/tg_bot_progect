from aiogram import Router
from aiogram import F
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


# Начало взаимодействия с ботом
@start_proc.message(Command('start'))
async def handle_start(message: Message):
    await message.reply('Choice the command:\n/start - show commands\n/add_data - add information about Your finance '
                        'condition\n/recommendation - to see recommendations\n/my_rate - to see Your rating')


# Непосредственное добавление данных в бд
@pull_data.message(WaitingState.WAIT)
async def handle_push(message: Message, is_content: bool, cell: str, obj):
    new_info = message.text
    if is_content:
        cell += '/n' + new_info
    else:
        cell = new_info
    obj.save()


# Добавление статистических данных
@pull_data.message(WaitingState.WAIT_STATS, F.text == 'gain')
async def new_gain(message: Message):
    return message.text


@pull_data.message(WaitingState.WAIT_STATS, F.text == 'cost')
async def new_cost(message: Message):
    return message.text


async def push_to_finance(id_user):
    count = 0
    for is_user in FINANCES:
        if is_user == id_user:
            FINANCES[count].gain.add(await new_gain())
            FINANCES[count].cost.add(await new_cost())
            break
        count += 1
    if count == len(FINANCES):
        FINANCES.add({'user_id': id_user, 'gain': await new_gain(), 'cost': await new_cost()})


@pull_data.message(Command('add_data'))
async def handle_pull(message: Message, state: FSMContext):
    user = message.from_user
    for stroke in User.select():
        if stroke.id_ != user.id:
            continue
        else:
            if not stroke.finance:
                await message.reply('Add new information')
                await state.set_state(WaitingState.WAIT)
                await handle_push(is_content=True, cell=stroke.finance, obj=stroke)
            else:
                await message.reply("There aren't information about You, please add it")
                await state.set_state(WaitingState.WAIT)
                await handle_push(is_content=False, cell=stroke.finance, obj=stroke)
            await state.set_state(WaitingState.WAIT_STATS)
            FINANCES.add({'user_id': user.id, 'gain': await new_gain(), 'cost': await new_cost()})
            await message.reply('Information was added')
            break
    await push_to_finance(user.id)
