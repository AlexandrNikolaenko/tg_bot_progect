import matplotlib.pyplot as plt
from aiogram import Router
from aiogram.types import Message, InputFile
from aiogram.filters.command import Command
from data.db import User
from aiogram.methods.send_photo import SendPhoto
import os

# Функционал для отображения рейтинга финансового состояния
per_rate_router = Router()


# Поиск пути к созданному графику
def find_file(user_id):
    name = f'tg-bot/states{user_id}.png'
    return os.path.abspath(name)


# Вывод графика как картинки в чат с ботом
@per_rate_router.message(Command('my_rate'))
async def handle_send_photo(message: Message):
    user = message.from_user.id
    for is_user in User.select():
        if is_user.id_ == user:
            if is_user.gain is not None and is_user.cost is not None:
                gain = list(map(int, is_user.gain.split('\n')))
                cost = list(map(int, is_user.cost.split('\n')))
                plt.plot([i for i in range(len(gain))], gain, [i for i in range(len(cost))], cost)
                plt.savefig(f'states{user}.png')
                photo = InputFile(f"tg-bot/states{user}.png")
                await message.reply_photo(photo=photo)
            else:
                await message.reply("You haven't own statistic, please add Your data")
            break

