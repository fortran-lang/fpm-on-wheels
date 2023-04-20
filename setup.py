import sys

from skbuild import setup

setup(
    name="fpm",
    version="0.7.0",
    description="Fortran Package Manager",
    author="Fortran-lang",
    license="MIT",
    python_requires=">=3.7",
    cmake_args=(
        ["-G", "MSYS Makefiles"] if sys.platform == "win32" else ["-G", "Ninja"]
    ),
    cmake_with_sdist=True,
)
