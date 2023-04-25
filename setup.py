import sys

from setuptools import find_packages
from skbuild import setup

CMAKE_GENERATOR = "Ninja" if sys.platform != "win32" else "MSYS Makefiles"

setup(
    cmake_args=(["-G", CMAKE_GENERATOR]),
    packages=find_packages(
        where="src",
    ),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "fpm=fpm:main",
        ],
    },
    cmake_with_sdist=True,
)
