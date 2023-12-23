import subprocess
import sys

from pytoolkit.scripts.helloserver import replace_host_and_port


def test_scripts_entrypoint():
    executables = ["helloserver"]
    for executable in executables:
        p = subprocess.run(f"{executable} --version", shell=True)
        if p.returncode != 0:
            sys.exit(1)


def test_replace_host_and_port():
    url = "http://example.org/path/to/api"
    assert replace_host_and_port(url) == 'https://chatai.tsingtao.com.cn:443/path/to/api'
