import hashlib
import time
import uuid

from typing import Mapping

import httpx
import typer

cmd = typer.Typer()


def make_sign(nonce: str, timestamp: str, secret: str) -> str:
    return hashlib.sha1((nonce + timestamp + secret).encode()).hexdigest()


def get_headers(pubkey: str, secret: str) -> Mapping[str, str]:
    nonce = uuid.uuid4().hex
    timestamp = str(int(time.time()))
    sign = make_sign(nonce, timestamp, secret)
    return {
        "Api-Auth-pubkey": pubkey,
        "Api-Auth-sign": sign,
        "Api-Auth-nonce": nonce,
        "Api-Auth-timestamp": timestamp,
    }


@cmd.command()
def bot_response(
    scheme: str = typer.Option("https"),
    endpoint: str = typer.Option("demo.laiye.com:8083"),
    _type: str = typer.Option("channels"),
    channelId: str = typer.Option(...,
                                  prompt=True),
    action: str = typer.Option("getReply"),
    version: str = typer.Option("v1alpha1"),
    agentId: str = typer.Option(None,
                                prompt=True),
    pubkey: str = typer.Option(None,
                               prompt=True),
    secret: str = typer.Option(None,
                               prompt=True),
    username: str = typer.Option(None,
                                 prompt=True),
    content: str = typer.Option(None,
                                prompt=True),
    debug: bool = typer.Option(False),
):
    url = f'{scheme}://{endpoint}/chatbot/{version}/agents/{agentId}/{_type}/{channelId}/{action}'
    headers = get_headers(pubkey, secret)
    body = {"username": username, "query": {"text": {"content": content, }}}

    resp = httpx.post(url, json=body, headers=dict(headers))
    if debug:
        print(f"{url}\n{body}\n{headers}\n{resp.text}")

    if not (200 <= resp.status_code < 400):
        typer.echo(f"调用失败, 原因: {resp.text}")
        typer.Exit(-1)

    for res in resp.json()['responses']:
        if 'text' in res['msgBody']:
            val = res['msgBody']['text']["content"]
            print(f'text: {val}')
        elif 'image' in res['msgBody']:
            val = res['msgBody']['image']["resourceUrl"]
            print(f'image: {val}')


def main():
    cmd()


if __name__ == '__main__':
    main()
