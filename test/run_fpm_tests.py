#! /usr/bin/env python3

import sys
from subprocess import run
import shutil

if len(sys.argv) < 2:
    print("Usage: python run_test_suite.py <fpm-tag>")
    sys.exit(1)

tag = sys.argv[1]
DIR = "fpm-source"
run(["git", "clone", "https://github.com/fortran-lang/fpm.git", DIR])
run(["git", "checkout", tag], cwd=DIR)
run(["fpm", "build"], cwd=DIR)
run(["fpm", "test"], cwd=DIR)
shutil.rmtree(DIR)
