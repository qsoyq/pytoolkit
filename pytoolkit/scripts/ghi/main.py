import logging

from typing import Optional

import typer

import pytoolkit.scripts.ghi.release

from pytoolkit.console.cmd import is_cmd_exists
from pytoolkit.console.message import error
from pytoolkit.scripts import version_callback

helptext = """
A Wrapper for github cli.

https://cli.github.com/
"""

cmd = typer.Typer(help=helptext)
cmd.add_typer(pytoolkit.scripts.ghi.release.cmd, name="release")


@cmd.callback(invoke_without_command=True)
def default(
    log_level: int = typer.Option(
        logging.INFO,
        "--log_level",
        envvar="log_level",
        help="日志级别, DEBUG:10, INFO: 20, WARNING: 30, ERROR:40",
    ),
    log_format: str = typer.Option(r"%(asctime)s %(levelname)s %(filename)s %(lineno)s %(message)s"),
    version: Optional[bool] = typer.Option(None, "--version", "-V", callback=version_callback),
):
    logging.basicConfig(level=log_level, format=log_format)
    if not is_cmd_exists("gh"):
        typer.echo(error("gh not found"))
        raise typer.Exit(-1)


def main():
    cmd()


if __name__ == "__main__":
    main()
