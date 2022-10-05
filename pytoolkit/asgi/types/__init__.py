import typing

import typing_extensions

MessageType = typing.MutableMapping[str, typing.Any]
ScopeType = typing.MutableMapping[str, typing.Any]
ReceiveType = typing.Callable[[], typing.Awaitable[MessageType]]
SendType = typing.Callable[[MessageType], typing.Awaitable[None]]


class ASGIAppProtocol(typing_extensions.Protocol):

    #　https://asgi.readthedocs.io/en/latest/specs/lifespan.html
    async def __call__(self, scope: ScopeType, receive: ReceiveType, send: SendType):
        pass


class LifespanType:
    main: str = "lifespan"

    startup: str = "lifespan.startup"
    startup_complete: str = "lifespan.startup.complete"
    startup_failed: str = "lifespan.startup.failed"

    shutdown: str = "lifespan.shutdown"
    shutdown_complete: str = "lifespan.shutdown.complete"
    shutdown_failed: str = "lifespan.shutdown.failed"
