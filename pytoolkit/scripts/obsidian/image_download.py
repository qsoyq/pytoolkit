import logging
import re

from concurrent.futures import Future, ThreadPoolExecutor
from pathlib import Path
from typing import Optional

import httpx
import typer

from pytoolkit.console.message import error_echo
from pytoolkit.scripts import version_callback

cmd = typer.Typer()
logger = logging.getLogger(__name__)


@cmd.command()
def run(
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
    image_format: list[str] = typer.Option(['jpeg',
                                            'jpg',
                                            'png'],
                                           help="支持的图片格式"),
    image_host: str = typer.Option("telegraph.19940731.xyz",
                                   '--image-host',
                                   help="图片链接主机名"),
    output: Path = typer.Option(Path("./dist/obsidian/images/"),
                                "--output",
                                '-o',
                                help="图片资源保存路径"),
    path: Path = typer.Argument(Path("."),
                                help="dir path"),
):
    """Download images resource from markdown files."""
    logging.basicConfig(level=log_level, format=log_format)
    if not path.exists() or not path.is_dir():
        error_echo("Directory does not exist")
        raise typer.Exit(1)

    if not output.exists():
        output.mkdir(parents=True)

    paths = iter_path(path)

    format_str = "|".join(image_format)
    format_pattern = f"({format_str})"
    pattern = re.compile(rf"(https?://{image_host}/file/\w+.{format_pattern})")

    urls: list[str] = []
    for path in paths:
        urls.extend(parse_file(path, pattern))

    with ThreadPoolExecutor() as executor:
        futures: list[Future] = []
        for url in urls:
            write_file_path = output / url.rsplit('/', 1)[-1]
            future = executor.submit(download_image, url, write_file_path)
            futures.append(future)
        for future in futures:
            future.result()


def iter_path(path: Path) -> list[Path]:
    pattern = '*'
    paths: list[Path] = []
    for p in path.rglob(pattern):
        s = str(p)
        if not s.endswith(".md"):
            continue
        if '.trash' in s:
            continue
        paths.append(p)
    return paths


def parse_file(path: Path, pattern: re.Pattern) -> list[str]:
    urls: list[str] = []
    with path.open('r') as f:
        for line in f.readlines():
            result: list[tuple[str, str]] = re.findall(pattern, line)
            if result:
                urls.extend([x[0] for x in result])
    return urls


def download_image(url: str, path: Path):
    resp = httpx.get(url)
    try:
        resp.raise_for_status()
    except httpx.HTTPStatusError as e:
        error_echo(f"{e}")
        raise e
    if not path.parent.exists():
        path.parent.mkdir(parents=True)
    with path.open('wb') as f:
        f.write(resp.content)


def main():
    cmd()


if __name__ == '__main__':
    main()
