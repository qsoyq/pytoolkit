import binascii
import logging
import os

from typing import Optional

import typer

from pytoolkit.scripts import version_callback

cmd = typer.Typer()
logger = logging.getLogger()


@cmd.command()
def run(
    size: int = typer.Option(16,
                             '--size',
                             '-s'),
    log_level: int = typer
    .Option(logging.INFO,
            '--log_level',
            envvar='log_level',
            help='日志级别, DEBUG:10, INFO: 20, WARNING: 30, ERROR:40'),
    log_format: str = typer.Option(r'%(asctime)s %(levelname)s %(filename)s %(lineno)s %(message)s'),
    version: Optional[bool] = typer.Option(None,
                                           "--version",
                                           "-V",
                                           callback=version_callback),
):
    """Return a bytestring of size random bytes suitable for cryptographic use."""
    logging.basicConfig(level=log_level, format=log_format)
    print(binascii.b2a_hex(os.urandom(size)).decode())


def main():
    cmd()


if __name__ == '__main__':
    main()
