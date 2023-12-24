import json
import logging

from pathlib import Path
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
    output_dir: Path = typer.Option(
        "./dist/openapi/examples/", "--dir", "-D", help="示例文件输出目录路径"
    ),
    url: str = typer.Argument(..., help="openapi.json url 地址"),
):
    """Export JSON examples corresponding to each API interface from the online openapi.json."""
    logging.basicConfig(level=log_level, format=log_format)
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    res = httpx.get(url)
    try:
        res.raise_for_status()
    except httpx.HTTPStatusError as e:
        logger.error(f"response headers: {res.headers}\nresponse text: {res.text}")
        raise e
    logger.debug(res.text)
    data = res.json()

    schemas = data.get("components", {}).get("schemas", {})
    path: str
    for path in data.get("paths", {}):
        for method in data["paths"][path]:
            for status_code in data["paths"][path][method]["responses"]:
                content = data["paths"][path][method]["responses"][status_code].get(
                    "content", {}
                )
                if "application/json" not in content:
                    continue

                schema = content["application/json"].get("schema", {})
                ref: str = schema.get("$ref", "")
                if not ref:
                    continue
                schema_name = ref.rsplit("/", 1)[-1]
                if schema_name not in schemas:
                    logging.warning(f"{schema_name} not in schemas")
                    continue
                title: str = schemas[schema_name].get("title", schema_name)
                example: dict | list = schemas[schema_name].get("example", {})
                json_str = json.dumps(example)

                output_path = (
                    output_dir
                    / Path(path.lstrip("/"))
                    / Path(method)
                    / Path(title + ".json")
                )
                logger.debug(f"output path: {output_path}")
                if not output_path.parent.exists():
                    output_path.parent.mkdir(parents=True)
                with output_path.open("w") as f:
                    f.write(json_str)


def main():
    cmd()


if __name__ == "__main__":
    main()
