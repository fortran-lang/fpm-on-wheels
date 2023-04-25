import platform
import subprocess
import sys
from pathlib import Path


def main():
    binary = Path(__file__).parent / "fpm"
    if platform.system() == "Windows":
        binary = binary.with_suffix(".exe")

    res = subprocess.run([binary] + sys.argv[1:])
    sys.exit(res.returncode)
