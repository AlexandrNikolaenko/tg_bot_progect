import matplotlib.pyplot as plt
from aiogram import Router
from aiogram.types import Message, InputFile
from aiogram.filters.command import Command
from data.db import FINANCES
from aiogram.methods.send_photo import SendPhoto
from glob import glob

# Функционал для отображения рейтинга финансового состояния
per_rate_router = Router()


# Поиск пути к созданному графику
def find_file(user_id):
    file_list = glob(f'states{user_id}.png')
    filename = file_list[0]
    return filename


# Создание графика изменения финансового состояния
def create_rate(user_id, index):
    gain = FINANCES[index]['gain']
    cost = FINANCES[index]['cost']
    plt.plot([i for i in range(len(gain))], gain, [i for i in range(len(cost))], cost)
    plt.savefig(f'sates{user_id}.png')


# Вывод графика как картинки в чат с ботом
@per_rate_router.message(Command('my_rate'))
async def handle_send_photo(message: Message):
    user = message.from_user.id
    index = 0
    for is_user in FINANCES:
        if is_user['user_id'] == user:
            break
        else:
            index += 1
    if index != len(FINANCES):
        create_rate(user, index)
        photo = InputFile(find_file(user))
        await SendPhoto(chat_id=message.chat.id, photo=photo)
    else:
        await message.reply("You haven't own statistic, please add Your data")
