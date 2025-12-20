#!/usr/bin/env python3
"""
Cross-platform test runner for fpm-on-wheels.
"""

import argparse
import logging
import os
import shlex
import shutil
import stat
import subprocess
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("run_tests")


def on_rm_error(func, path, exc_info):
    """Handle read-only files on Windows during cleanup."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def run(cmd, **kwargs):
    """Run a command, logging the invocation."""
    logger.info(f"+ {shlex.join(cmd)}")
    subprocess.check_call(cmd, **kwargs)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default="https://github.com/fortran-lang/fpm.git")
    parser.add_argument("--tag", default="v0.12.0")
    args = parser.parse_args()

    test_dir = Path("fpm-test").resolve()

    if test_dir.exists():
        logger.info(f"Cleaning {test_dir}")
        shutil.rmtree(test_dir, onerror=on_rm_error)

    run(
        [
            "git",
            "clone",
            "--depth",
            "1",
            "--branch",
            args.tag,
            args.repo,
            str(test_dir),
        ]
    )

    env = os.environ.copy()
    # Forward compiler variables to FPM_*
    for compiler in ["FC", "CC", "CXX"]:
        val = env.get(compiler)
        if val:
            env[f"FPM_{compiler}"] = val
            logger.info(f"Exporting FPM_{compiler}={val}")

    if not shutil.which("fpm", path=env.get("PATH")):
        logger.error("Executable 'fpm' not found in PATH.")
        sys.exit(1)

    run(["fpm", "test"], cwd=test_dir, env=env)


if __name__ == "__main__":
    main()
