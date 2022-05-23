from functools import wraps
from inspect import _void
from asgiref.sync import sync_to_async
from config.main_config import REACT
from . import func
from channels.auth import get_user

def currentUserAsync(foo) -> _void:
    """ Set current user for async funcs """
    @wraps(foo)
    async def wrapper(self, data, *args, **kwargs):
        if REACT:
            data['current_user'] = await sync_to_async(func.get_serializer_user_react,thread_sensitive=True)()
        else:
            data['current_user'] = await sync_to_async(func.serializer_user,thread_sensitive=True)(await get_user(self.scope))
        return await foo(self, data, *args, **kwargs)
    return wrapper