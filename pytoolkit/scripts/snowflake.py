import logging

from typing import List, Optional

import typer

from pytoolkit.message.snowflake import Snowflake
from pytoolkit.scripts import version_callback

cmd = typer.Typer()
logger = logging.getLogger()


@cmd.command()
def generate(
    workid: int = typer.Option(0,
                               '-w'),
    count: int = typer.Option(1,
                              '-c',
                              help='生成的数量'),
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
    for _ in range(count):
        print(Snowflake(workid=workid).generate())


def split(
    msgid_list: List[int] = typer.Argument(...,
                                           help='snowflake message id'),
    workid: int = typer.Option(0,
                               '-w'),
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
    for msgid in msgid_list:
        print(Snowflake(workid=workid).split(msgid))


def main():
    cmd()


if __name__ == '__main__':
    main()
