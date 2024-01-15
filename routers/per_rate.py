import matplotlib.pyplot as plt
from aiogram import Router
from aiogram.types import Message, InputFile
from aiogram.filters.command import Command
from data.db import User
from aiogram.methods.send_photo import SendPhoto
from glob import glob

# ���������� ��� ����������� �������� ����������� ���������
per_rate_router = Router()


# ����� ���� � ���������� �������
def find_file(user_id):
    file_list = glob(f'states{user_id}.png')
    filename = file_list[0]
    return filename


# ����� ������� ��� �������� � ��� � �����
@per_rate_router.message(Command('my_rate'))
async def handle_send_photo(message: Message):
    user = message.from_user.id
    for is_user in User.select():
        if is_user.id_ == user:
            if is_user.gain is not None and is_user.cost is not None:
                gain = list(map(int, is_user.gain.split('\n')))
                cost = list(map(int, is_user.cost.split('\n')))
                plt.plot([i for i in range(len(gain))], gain, [i for i in range(len(cost))], cost)
                plt.savefig(f'sates{user}.png')
                photo = InputFile(find_file(user))
                await SendPhoto(chat_id=message.chat.id, photo=photo)
            else:
                await message.reply("You haven't own statistic, please add Your data")
            break

