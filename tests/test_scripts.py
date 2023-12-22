import subprocess
import sys


def test_scripts_entrypoint():
    executables = ["helloserver"]
    for executable in executables:
        p = subprocess.run(f"{executable} --version", shell=True)
        if p.returncode != 0:
            sys.exit(1)
