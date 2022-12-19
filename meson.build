project(
  'fpm-pypi',
  version: '0.7.0',
)

pymod = import('python')
python = pymod.find_installation('python3')

fpm_prj = subproject(
  'fpm-@0@'.format(meson.project_version()),
  default_options: [
    'default_library=static',
    'appdir=@0@'.format(python.get_install_dir(pure: false, subdir: 'fpm'))
  ],
)
fpm_app = fpm_prj.get_variable('fpm_app')

python.install_sources(
  '__main__.py',
  subdir: 'fpm',
  pure: false,
)
