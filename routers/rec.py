from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from data.db import User

# ���� ���������� ������ ����� �������� � ChatGPT ��� ������������� ��� API �
# �������� ������������ ��� ��������� ���������� ��������

rec_router = Router()


class RecStates(StatesGroup):
    pass


