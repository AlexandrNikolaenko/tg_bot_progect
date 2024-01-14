from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from data.db import User


class UsersMiddlewares(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        username = event.from_user
        user = User.get_or_none(User.id_ == username.id)
        if user is None:
            user = User.create(
                id_=username.id,
                user_name=username.username,
                full_name=username.full_name
            )


        data['_user'] = user
        await handler(event, data)
