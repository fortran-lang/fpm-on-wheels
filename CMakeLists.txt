cmake_minimum_required(VERSION 3.19 FATAL_ERROR)

project(fpm LANGUAGES C CXX Fortran)

include(ExternalProject)
include(FetchContent)

# Set the default build type to Release
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Choose the type of build." FORCE)
endif()

# Set Git tags for dependencies
set(M_CLI2_TAG "7264878cdb1baff7323cc48596d829ccfe7751b8" CACHE STRING "Set git tag for M_CLI2")
set(JONQUIL_TAG "4fbd4cf34d577c0fd25e32667ee9e41bf231ece8" CACHE STRING "Set git tag for jonquil")
set(REGEX_TAG "1.1.2" CACHE STRING "Set git tag for Fortran-regex")
set(SHLEX_TAG "1.0.1" CACHE STRING "Set git tag for fortran-shlex")
set(FPM_VERSION "0.10.0" CACHE STRING "Set fpm version e.g. 8.0.0")
set(FPM_TAG "v${FPM_VERSION}" CACHE STRING "Set git tag for fpm, default is v${FPM_VERSION}")

set(BIN_NAME ${CMAKE_PROJECT_NAME})

find_package(OpenMP COMPONENTS Fortran)

FetchContent_Declare(
  fpm_src
  GIT_TAG ${FPM_TAG}
  GIT_REPOSITORY "https://github.com/fortran-lang/fpm.git"
  SOURCE_DIR "${CMAKE_BINARY_DIR}/fpm"
)
FetchContent_MakeAvailable(fpm_src)

# Download the dependencies from a git project
FetchContent_Declare(
  m_cli2_src
  GIT_REPOSITORY "https://github.com/urbanjost/M_CLI2.git"
  GIT_TAG ${M_CLI2_TAG}
  SOURCE_DIR "${CMAKE_BINARY_DIR}/dependencies/M_CLI2"
)

# Do not import any of the predefined targets from the dependencies
# FetchContent_Declare does not support EXCLUDE_FROM_ALL since all configuration
# options are disabled.
# A workaround is to set the global property EXCLUDE_FROM_ALL before calling
# see: https://gitlab.kitware.com/cmake/cmake/-/issues/20167
# Case 1: Set before (applies to current scope and below)
set_directory_properties(PROPERTIES EXCLUDE_FROM_ALL YES)

FetchContent_Declare(
  jonquil_src
  GIT_REPOSITORY "https://github.com/toml-f/jonquil.git"
  GIT_TAG ${JONQUIL_TAG}
  SOURCE_DIR "${CMAKE_BINARY_DIR}/dependencies/jonquil"
)

FetchContent_Declare(
  regex_src
  GIT_REPOSITORY "https://github.com/perazz/fortran-regex"
  GIT_TAG ${REGEX_TAG}
  SOURCE_DIR "${CMAKE_BINARY_DIR}/dependencies/fortran-regex"
)

FetchContent_Declare(
  shlex_src
  GIT_REPOSITORY "https://github.com/perazz/fortran-shlex.git"
  GIT_TAG ${SHLEX_TAG}
  SOURCE_DIR "${CMAKE_BINARY_DIR}/dependencies/fortran-shlex"
)

FetchContent_MakeAvailable(fpm_src m_cli2_src jonquil_src regex_src shlex_src)

# Get toml-f's source dir from within jonquil's source dir
# FetchContent_Declare is first come first serve in terms of target names
# so we cannot download toml-f directly since it is a dependency of jonquil
# Make custom find modules available for project
set(CMAKE_MODULE_PATH "${CMAKE_MODULE_PATH}" "${jonquil_src_SOURCE_DIR}/config/cmake")
find_package("toml-f" REQUIRED)

# Case 2: Set after (applies only to dependency's scope and below)
if(IS_DIRECTORY "${jonquil_src_SOURCE_DIR}")
  set_property(DIRECTORY ${jonquil_src_SOURCE_DIR} PROPERTY EXCLUDE_FROM_ALL YES)
endif()

message(STATUS "M_CLI2 source dir: ${m_cli2_src_SOURCE_DIR}")
message(STATUS "jonquil source dir: ${jonquil_src_SOURCE_DIR}")
message(STATUS "regex source dir: ${regex_src_SOURCE_DIR}")
message(STATUS "shlex source dir: ${shlex_src_SOURCE_DIR}")
message(STATUS "fpm source dir: ${fpm_src_SOURCE_DIR}")

# Collect source files
# In general not recommended but fpm has a small footprint and we control the sources
file(GLOB_RECURSE
  SRC_FILES
  ${m_cli2_src_SOURCE_DIR}/src/M_CLI2*.F90
  ${m_cli2_src_SOURCE_DIR}/src/M_CLI2*.f90
  ${jonquil_src_SOURCE_DIR}/src/*.f90
  ${TOML_FORTRAN_SOURCE_DIR}/src/*.f90
  ${regex_src_SOURCE_DIR}/src/*.f90
  ${shlex_src_SOURCE_DIR}/src/*.f90
  ${fpm_src_SOURCE_DIR}/src/*.f90
  ${fpm_src_SOURCE_DIR}/src/*.F90
  ${fpm_src_SOURCE_DIR}/src/*.h
  ${fpm_src_SOURCE_DIR}/src/*.c
)

# Make code position independent (-fPIC)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

add_executable(${BIN_NAME} ${SRC_FILES} ${fpm_src_SOURCE_DIR}/app/main.f90)

# version preproc tag was added in fpm 0.8.2
target_compile_definitions(${BIN_NAME} PRIVATE FPM_RELEASE_VERSION=${FPM_VERSION})

# HACK: circumvent compiler's default preprocessor heuristic and enable it
# globally. This is to circumvent sr/fpm/fpm_release.f90 erroneous lowecase
# file extension.
# Remove in the next fpm release
target_compile_options(${BIN_NAME} PRIVATE "-cpp")

if(OpenMP_Fortran_FOUND)
  message(STATUS "OpenMP Fortran found: Building fpm for parallel execution")
  target_link_libraries(${BIN_NAME} PUBLIC OpenMP::OpenMP_Fortran)
endif()

# Set additional properties for executable target
set_target_properties(${BIN_NAME}
  PROPERTIES
  OUTPUT_NAME ${PROJECT_NAME}

  RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin

  # Dump .mod files to src dir to not pollute the build dir
  Fortran_MODULE_DIRECTORY ${CMAKE_BINARY_DIR}/inc
)

# Install fpm inside the src layout for __main__.py to pick it up
install(TARGETS ${BIN_NAME}
  RUNTIME DESTINATION ${CMAKE_INSTALL_PREFIX}/src/fpm
)
