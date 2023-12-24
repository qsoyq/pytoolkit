"""来也消息路由接口

- 修改机器人回复中的图片主机地址
- 修改机器人回复中的视频主机地址
"""
import json
import logging

from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse, urlunparse

import typer
import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

from pytoolkit.scripts import version_callback

cmd = typer.Typer()
app = FastAPI()
logger = logging.getLogger(__name__)


@dataclass
class Settings:
    scheme: str = "https"
    host: str = "chatai.tsingtao.com.cn"
    port: str = "443"


settings = Settings()


def replace_host_and_port(url):
    s = settings
    parsed_url = urlparse(url)
    replaced_url = parsed_url._replace(netloc=f"{s.host}:{s.port}", scheme=s.scheme)
    new_url = urlunparse(replaced_url)
    return new_url


@app.get("/")
def index():
    return PlainTextResponse("success")


@app.post("/message-route")
async def message_route(req: Request):
    """
    - 修改机器人回复中的图片主机地址
    - 修改机器人回复中的视频主机地址
    """
    body = await req.body()
    bot_message = json.loads(body.decode())
    responses = bot_message["responses"]
    for response in responses:
        if "image" in response["msgBody"]:
            response["msgBody"]["image"]["resourceUrl"] = replace_host_and_port(
                response["msgBody"]["image"]["resourceUrl"]
            )
            logger.debug(f"new image: {response['msgBody']['image']['resourceUrl']}")
        if "video" in response["msgBody"]:
            response["msgBody"]["video"]["resourceUrl"] = replace_host_and_port(
                response["msgBody"]["video"]["resourceUrl"]
            )
            logger.debug(f"new video: {response['msgBody']['video']['resourceUrl']}")
    return bot_message


@cmd.command()
def http(
    host: str = typer.Option("0.0.0.0", "--host", "-h", envvar="http_host"),
    port: int = typer.Option(8000, "--port", "-p", envvar="http_port"),
    reload: bool = typer.Option(False, "--debug", envvar="http_reload"),
    log_level: int = typer.Option(logging.DEBUG, "--log_level", envvar="log_level"),
    version: Optional[bool] = typer.Option(
        None, "--version", "-V", callback=version_callback
    ),
):
    """启动 http 服务"""
    logging.basicConfig(level=log_level)
    logging.info(f"http server listening on {host}:{port}")
    module = "pytoolkit.scripts.helloserver"
    uvicorn.run(f"{module}:app", host=host, port=port, reload=reload)


def main():
    cmd()


if __name__ == "__main__":
    cmd()
