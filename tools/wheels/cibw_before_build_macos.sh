set -ex

PROJECT_DIR="$1"
PLATFORM="macosx-arm64"
PLAT="arm64"
source $PROJECT_DIR/tools/wheels/gfortran_utils.sh
install_gfortran
pip install "delocate==0.10.4"

echo "@@@ cross-compiler: " $FC_ARM64
echo "@@@ default compiler(FC): " $FC
echo "@@@ FC_ARM64_LDFLAGS: " $FC_ARM64_LDFLAGS
export LDFLAGS="$FC_ARM64_LDFLAGS:$LDFLAGS"
