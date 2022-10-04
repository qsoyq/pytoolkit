import asyncio.locks
import inspect
import threading

from functools import wraps
from typing import Callable, Union


def once(func: Callable):
    done = 0
    _lock: Union[threading.Lock, asyncio.locks.Lock]
    if not callable(func):
        raise TypeError("func must be callable")

    if inspect.iscoroutinefunction(func):
        _lock = asyncio.locks.Lock()

        @wraps(func)
        async def async_wrapped(*args, **kwargs):
            nonlocal _lock, done
            async with _lock:
                if done == 0:
                    try:
                        return await func(*args, **kwargs)
                    finally:
                        done = 1

        return async_wrapped

    _lock = threading.Lock()

    @wraps(func)
    def wrapped(*args, **kwargs):
        nonlocal _lock, done
        with _lock:
            if done == 0:
                try:
                    return func(*args, **kwargs)
                finally:
                    done = 1

    return wrapped
