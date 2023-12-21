import json
import logging

from typing import Optional
from urllib.parse import urlparse, urlunparse

import typer
import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

try:
    from pydantic import BaseSettings
except ImportError:
    from pydantic_settings import BaseSettings

from pytoolkit.scripts import version_callback

cmd = typer.Typer()
app = FastAPI()
logger = logging.getLogger(__name__)


class Settings(BaseSettings):  # type: ignore
    scheme: str = "https"
    host: str = "chatai.tsingtao.com.cn"
    port: str = "443"


def replace_host_and_port(url):
    s = Settings()
    parsed_url = urlparse(url)
    replaced_url = parsed_url._replace(netloc=f"{s.host}:{s.port}", scheme=s.scheme)
    new_url = urlunparse(replaced_url)
    return new_url


@app.get('/')
def index():
    return PlainTextResponse("success")


@app.post('/message-route')
async def message_route(req: Request):
    body = await req.body()
    bot_message = json.loads(body.decode())
    responses = bot_message['responses']
    for response in responses:
        # if 'text' in response['msgBody']:
        #     response['msgBody']['text']['content'] = f"{response['msgBody']['text']['content']}_"
        if 'image' in response['msgBody']:
            response['msgBody']['image']['resourceUrl'] = replace_host_and_port(
                response['msgBody']['image']['resourceUrl']
            )
            logger.debug(f"new image: {response['msgBody']['image']['resourceUrl']}")
        if 'video' in response['msgBody']:
            response['msgBody']['video']['resourceUrl'] = replace_host_and_port(
                response['msgBody']['video']['resourceUrl']
            )
            logger.debug(f"new video: {response['msgBody']['video']['resourceUrl']}")
    return bot_message


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
    version: Optional[bool] = typer.Option(None,
                                           "--version",
                                           "-V",
                                           callback=version_callback),
    name: str = typer.Option("",
                             '--name'),
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
