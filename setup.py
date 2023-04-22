import sys

from skbuild import setup

CMAKE_GENERATOR = "Ninja" if sys.platform != "win32" else "MSYS Makefiles"

setup(
    cmake_args=(["-G", CMAKE_GENERATOR]),
    cmake_with_sdist=True,
)
