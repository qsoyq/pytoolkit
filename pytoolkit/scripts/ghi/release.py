import logging
import shlex
import subprocess

from pathlib import Path
from typing import Optional

import toml
import typer

cmd = typer.Typer(help='A Wrapper for github cli release command.')

logger = logging.getLogger()


@cmd.command()
def create(
    tag: Optional[str] = typer.Option(None,
                                      '--tag'),
    title: str = typer.Option("",
                              '-t',
                              '--title',
                              help='Release title'),
    target: str = typer.Option('',
                               '--target',
                               help='Target branch or full commit SHA (default: main branch)'),
    notes: str = typer.Option("",
                              "--notes",
                              '-n',
                              help='Release notes'),
    prerelease: Optional[bool] = typer.Option(None,
                                              '-p',
                                              '--prerelease ',
                                              help='Mark the release as a prerelease'),
    verbose: Optional[bool] = typer.Option(
        None,
        '--verbose',
    ),
):
    """Create a new GitHub Release for a repository."""
    # TODO: add release assets
    cmd = "gh release create"
    if notes:
        cmd += f" --notes {notes}"
    else:
        cmd += ' --generate-notes'

    if prerelease:
        cmd += " --prerelease"

    if target:
        cmd += f" --target {target}"

    if title:
        cmd += f" -t {title}"

    if tag is None:
        config_path = Path("pyproject.toml")
        if not config_path.exists():
            logger.warning("pyproject.yaml is not exists.")
            raise typer.Exit(1)

        document = toml.load(config_path)
        logger.debug(f"document: {document}")
        try:
            version = document["tool"]["poetry"]["version"]
        except KeyError:
            logger.warning("version is not found in pyproject.toml")
            raise typer.Exit(1)

        if not isinstance(version, str):
            raise typer.Exit(1)

        if version.startswith('v'):
            tag = version
        else:
            tag = f'v{version}'

    cmd += f" {tag}"
    args = shlex.split(cmd)
    if verbose:
        typer.echo(f"cmd: {cmd}")

    p = subprocess.run(args, capture_output=True, text=True)
    if p.returncode != 0:
        typer.echo(p.stderr, err=True, color=True)
        raise typer.Exit(p.returncode)

    typer.echo(p.stdout)


@cmd.command()
def delete(
    tag: Optional[str] = typer.Option(None,
                                      '--tag'),
    verbose: Optional[bool] = typer.Option(
        None,
        '--verbose',
    ),
    skip_prompt: bool = typer.Option(True,
                                     '-y',
                                     '--yes',
                                     help='Skip the confirmation prompt'),
):
    """Delete a release."""
    cmd = "gh release delete"

    if tag is None:
        config_path = Path("pyproject.toml")
        if not config_path.exists():
            logger.warning("pyproject.yaml is not exists.")
            raise typer.Exit(1)

        document = toml.load(config_path)
        logger.debug(f"document: {document}")
        try:
            version = document["tool"]["poetry"]["version"]
        except KeyError:
            logger.warning("version is not found in pyproject.toml")
            raise typer.Exit(1)

        if not isinstance(version, str):
            raise typer.Exit(1)

        if version.startswith('v'):
            tag = version
        else:
            tag = f'v{version}'

    if skip_prompt:
        cmd += ' -y'

    cmd += f" {tag}"
    args = shlex.split(cmd)
    if verbose:
        typer.echo(f"cmd: {cmd}")

    p = subprocess.run(args, capture_output=True, text=True)
    if p.returncode != 0:
        typer.echo(p.stderr, err=True, color=True)
        raise typer.Exit(p.returncode)
    # TODO: delete tag
    typer.echo(p.stdout)


def main():
    cmd()


if __name__ == '__main__':
    main()
