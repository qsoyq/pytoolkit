import json
import logging

from typing import Optional

import httpx
import typer

from pytoolkit.scripts import version_callback

cmd = typer.Typer()
logger = logging.getLogger(__name__)


@cmd.command()
def run(
    log_level: int = typer.Option(
        logging.INFO,
        "--log_level",
        envvar="log_level",
        help="日志级别, DEBUG:10, INFO: 20, WARNING: 30, ERROR:40",
    ),
    log_format: str = typer.Option(
        r"%(asctime)s %(levelname)s %(filename)s %(lineno)s %(message)s"
    ),
    version: Optional[bool] = typer.Option(
        None, "--version", "-V", callback=version_callback
    ),
    openapi_title: Optional[str] = typer.Option(
        "OpenAPI", "--title", "-t", envvar="openapi_title"
    ),
    openapi_verison: Optional[str] = typer.Option(
        "3.1.0", "--openapi-verison", envvar="openapi_verison"
    ),
    openapi_info_verison: Optional[str] = typer.Option(
        "1.0.0", "--openapi-info-verison", envvar="openapi_info_verison"
    ),
    urls: list[str] = typer.Argument(..., help="openapi.json url 地址"),
):
    """Merge multiple OpenAPI description files into one."""
    logging.basicConfig(level=log_level, format=log_format)
    fastapi_default_schemas = ["HTTPValidationError", "ValidationError"]
    paths = {}
    schemas = {}
    openapi_schema = {
        "openapi": openapi_verison,
        "info": {
            "title": openapi_title,
            "version": openapi_info_verison,
        },
        "paths": paths,
        "components": {
            "schemas": schemas,
        },
    }
    for url in urls:
        res = httpx.get(url)
        try:
            res.raise_for_status()
        except httpx.HTTPStatusError as e:
            logger.error(f"response headers: {res.headers}\nresponse text: {res.text}")
            raise e

        logger.debug(res.text)
        resp = res.json()

        already_exists = [
            x
            for x in resp.get("components", {}).get("schemas", {}).keys()
            if x in schemas
        ]
        already_exists = [x for x in already_exists if x not in fastapi_default_schemas]
        if already_exists:
            typer.echo(f"already exists components: {already_exists}", err=True)
            raise typer.Exit(-1)

        paths.update(resp.get("paths", {}))
        schemas.update(resp.get("components", {}).get("schemas", {}))

    typer.echo(json.dumps(openapi_schema))


def main():
    cmd()


if __name__ == "__main__":
    main()
