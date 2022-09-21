import shlex
import subprocess

from pathlib import Path
from typing import Optional

import toml
import typer

cmd = typer.Typer(help='A Wrapper for github cli release command.')


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
            typer.echo("pyproject.yaml is not exists.")
            raise typer.Exit(1)

        document = toml.load(config_path)
        try:
            version = document["tool"]["poetry"]["version"]
        except KeyError:
            typer.echo("version is not found in pyproject.toml")
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
    delete_tag: bool = typer.Option(True,
                                    '--delete-tag'),
):
    """Delete a release."""
    cmd = "gh release delete"
    if tag is None:
        config_path = Path("pyproject.toml")
        if not config_path.exists():
            typer.echo("pyproject.yaml is not exists.")
            raise typer.Exit(1)

        document = toml.load(config_path)
        try:
            version = document["tool"]["poetry"]["version"]
        except KeyError:
            typer.echo("version is not found in pyproject.toml")
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

    typer.echo(p.stdout)
    if not delete_tag:
        return

    cmd = f'git tag -d {tag}'
    p = subprocess.run(shlex.split(cmd), capture_output=True, text=True)

    cmd = f'git push origin :refs/tags/{tag}'
    p = subprocess.run(shlex.split(cmd), capture_output=True, text=True)
    if p.returncode != 0:
        typer.echo(p.stderr, err=True, color=True)
        raise typer.Exit(p.returncode)


def main():
    cmd()


if __name__ == '__main__':
    main()
