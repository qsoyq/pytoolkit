import subprocess


def is_cmd_exists(executable: str) -> bool:
    p = subprocess.run(f"command -v {executable}", shell=True, capture_output=True)
    return p.returncode == 0
