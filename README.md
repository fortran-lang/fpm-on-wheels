# fpm-on-wheels

This project is responsible for generating the wheels and the source
distribution for the fpm project that is uploaded to PyPI.

The wheels are generated with `CMake`, `scikit-build` and `cibuildwheel`,
using a GNU Fortran (gfortran) compiler. They are also equipped by default
with OpenMP support, for parallel compilation.

## Supported platforms

The wheels are generated for the following platforms:

| Python version | Operating System | Architecture          |
| -------------- | ---------------- | --------------------- |
| >= 3.7         | Linux            | x86_64, i686, aarch64 |
| >= 3.7         | macOS            | x86_64, arm64         |
| >= 3.7         | Windows          | x86_64                |

## Release Instructions

1. Update the git tags and/or git commit IDs in `CMakeLists.txt` for:
   [`fpm`](https://github.com/fortran-lang/fpm.git),
   [`jonquil`](https://github.com/toml-f/jonquil.git),
   [`M_CLI2`](https://github.com/urbanjost/M_CLI2.git),
   [`fortran-regex`](https://github.com/perazz/fortran-regex.git) and
   [`fortran-shlex`](https://github.com/perazz/fortran-shlex.git).
2. Update the `docs/README.md` with the README file of the fpm project
3. Commit the changes via a pull-request to `main` and ask one of the admins
   to merge it.
4. Admins: Issue a new release on GitHub with the same version number as
   in `pyproject.toml` using the prefix `v` e.g. `v0.1.0`.

## Development Instructions

Ensure that the following scripts and license notices are up to date:

- `tools/wheels/gfortran_utils.sh` from <https://github.com/MacPython/gfortran-install>
