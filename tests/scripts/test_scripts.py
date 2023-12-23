import subprocess
import sys


def test_scripts_entrypoint():
    executables = [
        "snowflake",
        "urandom",
        "ghi",
        "ghi release create",
        "ghi release delete",
        "helloserver",
        "lc-chatbot",
        "laiye-web-message-route-tsingtao",
        "openapi_download",
        "openapi_aggerator",
        "obsidian_image_download",
        "obsidian_assets_download",
    ]
    for executable in executables:
        p = subprocess.run(f"{executable} --version", shell=True)
        if p.returncode != 0:
            sys.exit(1)
