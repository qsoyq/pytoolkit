import typer

from pytoolkit import __version__, __package__


def version_callback(value: bool):
    if value:
        print(f"{__package__} CLI Version: {__version__}")
        raise typer.Exit()
