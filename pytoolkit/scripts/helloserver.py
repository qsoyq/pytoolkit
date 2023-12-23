import logging

from typing import Optional

import typer
import uvicorn

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from pytoolkit.scripts import version_callback

cmd = typer.Typer()
app = FastAPI()
logger = logging.getLogger(__name__)


@app.get('/')
def index():
    return PlainTextResponse("success")


@cmd.command()
def http(
    host: str = typer.Option("0.0.0.0",
                             '--host',
                             '-h',
                             envvar='http_host'),
    port: int = typer.Option(8000,
                             '--port',
                             '-p',
                             envvar='http_port'),
    reload: bool = typer.Option(True,
                                '--debug',
                                envvar='http_reload'),
    log_level: int = typer.Option(logging.DEBUG,
                                  '--log_level',
                                  envvar='log_level'),
    version: Optional[bool] = typer.Option(None,
                                           "--version",
                                           "-V",
                                           callback=version_callback)
):
    """启动 http 服务"""
    logging.basicConfig(level=log_level)
    logging.info(f"http server listening on {host}:{port}")
    module = 'pytoolkit.scripts.helloserver'
    uvicorn.run(f"{module}:app", host=host, port=port, reload=reload)


def main():
    cmd()


if __name__ == '__main__':
    cmd()
