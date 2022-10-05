import asyncio

import httpx
import pytest

from fastapi import FastAPI

from pytoolkit.asgi.events.lifespan import LifespanEvent


@pytest.mark.asyncio
async def test_httpx_asgi_transport():
    app = FastAPI()

    n = 0

    @app.get('/')
    def _():
        nonlocal n
        n += 1
        return {}

    client = httpx.AsyncClient(app=app)
    url = 'http://address/'

    assert n == 0
    await client.get(url)
    assert n == 1


@pytest.mark.asyncio
async def test_lifespan():
    app = FastAPI()
    is_running = False

    @app.on_event("startup")
    async def _():
        nonlocal is_running
        is_running = True

    @app.on_event("shutdown")
    async def _():
        nonlocal is_running
        is_running = False

    loop = asyncio.get_event_loop()
    lifespan = LifespanEvent(app, loop)  # type:ignore

    assert is_running is False
    await lifespan.startup()
    assert is_running is True
    await lifespan.shutdown()
    assert is_running is False

    async with lifespan:
        assert is_running is True
    assert is_running is False

    with pytest.raises(RuntimeError):
        async with lifespan:
            assert is_running is True
            raise RuntimeError()

    assert is_running is False
