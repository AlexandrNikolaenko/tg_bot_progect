from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command
from data.db import User
import g4f

# ���� ���������� ������ ����� �������� � ChatGPT ��� ������������� ��� API �
# �������� ������������ ��� ��������� ���������� ��������

rec_router = Router()


async def create_rec(message: Message, text):
    response = g4f.ChatCompletion.create(
        model=g4f.models.default,
        messages=[{"role": "user", "content": 'Please help me to improve my finance situation:\n' + text}],
    )
    return await message.reply(response)


@rec_router.message(Command('recommendation'))
async def get_rec(message: Message):
    await message.reply('Please wait a little')
    user = message.from_user
    stroke = dict()
    for is_user in User.select():
        if is_user.id_ == user.id:
            stroke = is_user
    if stroke.finance:
        await create_rec(message, stroke.finance)
    else:
        await message.reply("I'm sorry, but You didn't describe Your financial situation")
    return
