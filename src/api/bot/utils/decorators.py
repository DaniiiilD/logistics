import functools
from aiogram import types

def delete_user_message(func):
    @functools.wraps(func)
    async def wrapper(event, *args, **kwargs):
        if isinstance(event, types.Message):
            try: 
                await event.delete()
            except Exception:
                pass
            
        return await func(event, *args, **kwargs)
    return wrapper