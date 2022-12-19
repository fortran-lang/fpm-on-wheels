project(
  'M_CLI2',
  'fortran',
  version: '1.0.0',
)

m_cli2_lib = library(
  meson.project_name(),
  sources: files(
    'src' / 'M_CLI2.F90',
  ),
)

m_cli2_dep = declare_dependency(
  link_with: m_cli2_lib,
)
