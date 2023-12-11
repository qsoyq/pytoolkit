import typer


def error(message: str) -> str:
    return typer.style(message, fg=typer.colors.WHITE, bg=typer.colors.RED)


def error_echo(message: str):
    typer.echo(error(message))
