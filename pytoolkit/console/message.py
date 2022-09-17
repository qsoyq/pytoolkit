import typer


def error(message: str) -> str:
    return typer.style(message, fg=typer.colors.WHITE, bg=typer.colors.RED)
