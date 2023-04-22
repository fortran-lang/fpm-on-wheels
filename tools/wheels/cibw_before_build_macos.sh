set -ex

PROJECT_DIR="$1"
PLATFORM="macosx-arm64"
PLAT="arm64"
source $PROJECT_DIR/tools/wheels/gfortran_utils.sh
install_gfortran

# Cannot pass these variables to the wheel building process since before-build
# executes in a subprocess. So we print them out and manually set them in
# pyproject.toml
echo "@@@ FC:" $FC
echo "@@@ FC_ARM64_LDFLAGS:" $FC_ARM64_LDFLAGS
