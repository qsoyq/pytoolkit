import logging

import typer
import uvicorn

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

cmd = typer.Typer()
app = FastAPI()


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
    debug: bool = typer.Option(False,
                               '--debug',
                               envvar='http_debug'),
    reload: bool = typer.Option(False,
                                '--debug',
                                envvar='http_reload'),
    log_level: int = typer.Option(logging.DEBUG,
                                  '--log_level',
                                  envvar='log_level'),
    name: str = typer.Option("",
                             '--name'),
):
    """启动 http 服务"""
    logging.basicConfig(level=log_level)
    logging.info(f"http server listening on {host}:{port}")
    module = 'pytoolkit.scripts.helloserver'
    uvicorn.run(f"{module}:app", host=host, port=port, debug=debug, reload=reload)


def main():
    cmd()


if __name__ == '__main__':
    cmd()
