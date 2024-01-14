from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command
from data.db import User
import g4f

# Этот функционал должен будет общаться с ChatGPT или испоьльзовать его API и
# получать рекомендации для улучшения финансовой ситуации

rec_router = Router()


async def create_rec(message: Message, text):
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=[{"role": "user", "content": '' + text}],
    )
    await message.reply(response)


@rec_router.message(Command('recommendation'))
async def get_rec(message: Message):
    user = message.from_user
    stroke = dict()
    for is_user in User.select():
        if is_user.id_ == user.id:
            stroke = is_user
    if stroke.finance:
        await create_rec(message, stroke.finance)
    else:
        await message.reply("I'm sorry, but You didn't describe Your financial situation")
