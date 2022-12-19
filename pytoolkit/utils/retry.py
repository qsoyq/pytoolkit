import asyncio
import inspect
import time

from functools import partial, wraps
from typing import Callable, Optional, Tuple, Type, Union


def retry(
    func: Optional[Callable] = None,
    *,
    max_tries: int = 2,
    wait_secs: float = 1,
    exceptions: Union[Type,
                      Tuple[Type]] = BaseException
) -> Callable:
    if func is None:
        return partial(retry, max_tries=max_tries, wait_secs=wait_secs, exceptions=exceptions)

    if inspect.iscoroutinefunction(func):

        @wraps(func)
        async def async_retry_decorator(*args, **kwargs):
            tries = 1
            while True:
                tries += 1
                try:
                    return await func(*args, **kwargs)
                except exceptions as error:
                    if tries <= max_tries:
                        await asyncio.sleep(wait_secs)
                    else:
                        raise error

        return async_retry_decorator

    @wraps(func)
    def retry_decorator(*args, **kwargs):
        tries = 0
        while True:
            tries += 1
            try:
                return func(*args, **kwargs)
            except exceptions as error:
                if tries < max_tries:
                    time.sleep(wait_secs)
                else:
                    raise error

    return retry_decorator
