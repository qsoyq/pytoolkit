import asyncio
import logging

from typing import Optional

from pytoolkit.asgi.types import ASGIAppProtocol, LifespanType, MessageType

logger = logging.getLogger()


class LifespanEvent:
    """通过 Lifespan 管理 ASGIApplication 的启动和退出事件"""

    def __init__(
        self,
        app: ASGIAppProtocol,
        loop: Optional[asyncio.events.AbstractEventLoop] = None,
    ):
        self.app = app
        self.loop = loop if loop is not None else asyncio.get_event_loop()
        self.receive_queue: asyncio.Queue[MessageType] = asyncio.Queue()
        self.startup_event = asyncio.Event()
        self.shutdown_event = asyncio.Event()
        self.main_task: Optional[asyncio.Task] = None

    async def __aenter__(self):
        await self.startup()

    async def __aexit__(self, exc_type, exc_value, tb):
        await self.shutdown()
        if exc_type is not None:
            raise exc_type

    async def receive(self) -> MessageType:
        return await self.receive_queue.get()

    async def send(self, message: MessageType):
        body = message.get("message")
        assert message["type"] in (
            "lifespan.startup.complete",
            "lifespan.startup.failed",
            "lifespan.shutdown.complete",
            "lifespan.shutdown.failed",
        )
        startup_events = (LifespanType.startup_complete, LifespanType.startup_failed)
        if message["type"] in startup_events:
            assert not self.startup_event.is_set() and not self.shutdown_event.is_set()
            self.startup_event.set()

            if message["type"] == LifespanType.startup_failed:
                logger.debug(f"startup_failed: {body}")

        shutdown_events = (LifespanType.shutdown_complete, LifespanType.shutdown_failed)
        if message["type"] in shutdown_events:
            assert self.startup_event.is_set() and not self.shutdown_event.is_set()
            self.shutdown_event.set()

            if message["type"] == LifespanType.shutdown_failed:
                logger.debug(f"shutdown_failed: {body}")

    async def startup(self):
        self.main_task = self.loop.create_task(self.main())
        startup_event = {"type": LifespanType.startup}
        await self.receive_queue.put(startup_event)
        await self.startup_event.wait()

    async def shutdown(self):
        shutdown_event = {"type": LifespanType.shutdown}
        await self.receive_queue.put(shutdown_event)
        await self.shutdown_event.wait()
        if self.main_task and not self.main_task.cancelled:
            self.main_task.cancel()

        self.startup_event.clear()
        self.shutdown_event.clear()

    async def main(self):
        scope = {
            "type": LifespanType.main,
            "asgi": {"version": "asgi3", "spec_version": "2.0"},
        }
        await self.app(scope, self.receive, self.send)
