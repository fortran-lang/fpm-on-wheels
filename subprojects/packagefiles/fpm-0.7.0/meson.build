project(
  'fpm',
  'fortran', 'c',
  version: '0.7.0',
)

tomlf_dep = dependency(
  'toml-f',
  version: '>=0.3.1',
  fallback: ['toml-f-0.3.1', 'tomlf_dep'],
  default_options: [
    'default_library=static',
  ],
)

m_cli2_dep = dependency(
  'M_CLI2',
  version: '>=1.0.0',
  fallback: ['M_CLI2-7264878cdb1baff7323cc48596d829ccfe7751b8', 'm_cli2_dep'],
  default_options: [
    'default_library=static',
  ],
)

fpm_lib = library(
  meson.project_version(),
  sources: files(
    # fpm-0.7.0/src/:
    'src' / 'filesystem_utilities.c',
    'src' / 'fpm_backend_console.f90',
    'src' / 'fpm_backend.F90',
    'src' / 'fpm_backend_output.f90',
    'src' / 'fpm_command_line.f90',
    'src' / 'fpm_compiler.f90',
    'src' / 'fpm_environment.f90',
    'src' / 'fpm.f90',
    'src' / 'fpm_filesystem.F90',
    'src' / 'fpm_model.f90',
    'src' / 'fpm_os.F90',
    'src' / 'fpm_source_parsing.f90',
    'src' / 'fpm_sources.f90',
    'src' / 'fpm_strings.f90',
    'src' / 'fpm_targets.f90',
    # fpm-0.7.0/src/fpm:
    'src' / 'fpm' / 'dependency.f90',
    'src' / 'fpm' / 'error.f90',
    'src' / 'fpm' / 'git.f90',
    'src' / 'fpm' / 'installer.f90',
    'src' / 'fpm' / 'manifest.f90',
    'src' / 'fpm' / 'toml.f90',
    'src' / 'fpm' / 'versioning.f90',
    # fpm-0.7.0/src/fpm/cmd:
    'src' / 'fpm' / 'cmd' / 'install.f90',
    'src' / 'fpm' / 'cmd' / 'new.f90',
    'src' / 'fpm' / 'cmd' / 'update.f90',
    # fpm-0.7.0/src/fpm/manifest:
    'src' / 'fpm' / 'manifest' / 'build.f90',
    'src' / 'fpm' / 'manifest' / 'dependency.f90',
    'src' / 'fpm' / 'manifest' / 'example.f90',
    'src' / 'fpm' / 'manifest' / 'executable.f90',
    'src' / 'fpm' / 'manifest' / 'install.f90',
    'src' / 'fpm' / 'manifest' / 'library.f90',
    'src' / 'fpm' / 'manifest' / 'package.f90',
    'src' / 'fpm' / 'manifest' / 'preprocess.f90',
    'src' / 'fpm' / 'manifest' / 'profiles.f90',
    'src' / 'fpm' / 'manifest' / 'test.f90',
    # fpm-0.7.0/src/ptycheck:
    'src' / 'ptycheck' / 'isatty.c',
    'src' / 'ptycheck' / 'iscygpty.c',
    'src' / 'ptycheck' / 'iscygpty.h',
  ),
  dependencies: [tomlf_dep, m_cli2_dep],
)

fpm_dep = declare_dependency(
  link_with: fpm_lib,
  dependencies: [tomlf_dep, m_cli2_dep],
)

fpm_app = executable(
  meson.project_name(),
  sources: files(
    'app' / 'main.f90',
  ),
  dependencies: fpm_dep,
  install: true,
  install_dir: get_option('appdir'),
)
