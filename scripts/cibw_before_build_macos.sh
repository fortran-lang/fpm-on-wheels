# Install GFortran

if [[ $PLATFORM == "macosx-x86_64" ]]; then
  #GFORTRAN=$(type -p gfortran-9)
  #sudo ln -s $GFORTRAN /usr/local/bin/gfortran
  # same version of gfortran as the openblas-libs and scipy-wheel builds
  curl -L https://github.com/isuruf/gcc/releases/download/gcc-11.3.0-2/gfortran-darwin-x86_64-native.tar.gz -o gfortran.tar.gz

  GFORTRAN_SHA256=$(shasum -a 256 gfortran.tar.gz)
  KNOWN_SHA256="981367dd0ad4335613e91bbee453d60b6669f5d7e976d18c7bdb7f1966f26ae4  gfortran.tar.gz"
  if [ "$GFORTRAN_SHA256" != "$KNOWN_SHA256" ]; then
    echo sha256 mismatch
    exit 1
  fi

  sudo mkdir -p /opt/
  # places gfortran in /opt/gfortran-darwin-x86_64-native. There's then
  # bin, lib, include, libexec underneath that.
  sudo tar -xv -C /opt -f gfortran.tar.gz

  # Link these into /usr/local so that there's no need to add rpath or -L
  for f in libgfortran.dylib libgfortran.5.dylib libgcc_s.1.dylib libgcc_s.1.1.dylib libquadmath.dylib libquadmath.0.dylib; do
    ln -sf /opt/gfortran-darwin-x86_64-native/lib/$f /usr/local/lib/$f
  done
  ln -sf /opt/gfortran-darwin-x86_64-native/bin/gfortran /usr/local/bin/gfortran

  # Set SDKROOT env variable if not set
  # This step is required whenever the gfortran compilers sourced from
  # conda-forge (built by isuru fernando) are used outside of a conda-forge
  # environment (so it mirrors what is done in the conda-forge compiler
  # activation scripts)
  export SDKROOT=${SDKROOT:-$(xcrun --show-sdk-path)}
  gfortran tools/wheels/test.f
fi
