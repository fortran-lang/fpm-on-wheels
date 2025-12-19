# Notes

These scripts were taken and adapted from the MacPython gfortran-install
<https://github.com/MacPython/gfortran-install>
in order to perform cross-compilation for MacOS. The integration would happen
on the `pyproject.toml` side with `cibuildwheel` and `scikit-build`.

The integration looked something like this:

```toml

[[tool.cibuildwheel.overrides]]
select = "*-macosx_arm64"
before-build = "bash {project}/tools/wheels/cibw_before_build_macos.sh {project}"

# Override the default environment variables with the cross-compiled ones
[tool.cibuildwheel.overrides.environment]
CC = "clang"
CXX = "clang++"
FC = "/opt/gfortran-darwin-arm64-cross/bin/arm64-apple-darwin20.0.0-gfortran"
LDFLAGS = "-L/opt/gfortran-darwin-arm64-cross/lib/gcc/arm64-apple-darwin20.0.0/11.3.0 -Wl,-rpath,/opt/gfortran-darwin-arm64-cross/lib/gcc/arm64-apple-darwin20.0.0/11.3.0"
```
