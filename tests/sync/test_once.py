import asyncio
import time

from threading import Thread

import pytest

from pytoolkit.sync.once import once


def test():
    with pytest.raises(TypeError) as exc_info:
        once(1)  # type: ignore

    assert str(exc_info.value) == "func must be callable"

    n = 0

    @once
    def worker():
        nonlocal n
        n += 1

    for _ in range(10):
        worker()
        assert n == 1


def test_concurrency():
    n = 0

    @once
    def worker():
        nonlocal n
        time.sleep(1)
        n += 1

    _ts = [Thread(target=worker) for _ in range(10)]
    for t in _ts:
        t.start()

    for t in _ts:
        t.join()

    assert n == 1


@pytest.mark.asyncio
async def test_async_concurrency():
    n = 0

    @once
    async def worker():
        nonlocal n
        time.sleep(1)
        n += 1

    tasks = [worker() for _ in range(10)]
    await asyncio.gather(*tasks)

    assert n == 1
