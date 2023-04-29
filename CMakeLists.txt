cmake_minimum_required(VERSION 3.19 FATAL_ERROR)

project(fpm LANGUAGES C CXX Fortran)

include(ExternalProject)
include(FetchContent)

# Set the default build type to Release
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Choose the type of build." FORCE)
endif()

# Set Git tags for dependencies
set(M_CLI2_TAG "ea6bbffc1c2fb0885e994d37ccf0029c99b19f24" CACHE STRING "Set git tag for M_CLI2")
set(TOML_F_TAG "2f5eaba864ff630ba0c3791126a3f811b6e437f3" CACHE STRING "Set git tag for toml_f")
set(FPM_TAG "v0.5.0" CACHE STRING "Set git tag for fpm")

set(BIN_NAME ${CMAKE_PROJECT_NAME})

find_package(OpenMP REQUIRED Fortran)

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
  SOURCE_DIR "${fpm_src_SOURCE_DIR}/dependencies/M_CLI2"
)

# Do not import any of the predefined targets from the dependencies
# FetchContent_Declare does not support EXCLUDE_FROM_ALL since all configuration
# options are disabled.
# A workaround is to set the global property EXCLUDE_FROM_ALL before calling
# see: https://gitlab.kitware.com/cmake/cmake/-/issues/20167
# Case 1: Set before (applies to current scope and below)
set_directory_properties(PROPERTIES EXCLUDE_FROM_ALL YES)

FetchContent_Declare(
  toml_f_src
  GIT_REPOSITORY "https://github.com/toml-f/toml-f.git"
  GIT_TAG ${TOML_F_TAG}
  SOURCE_DIR "${fpm_src_SOURCE_DIR}/dependencies/toml-f"
)

FetchContent_MakeAvailable(m_cli2_src toml_f_src)

# Case 2: Set after (applies only to dependency's scope and below)
if(IS_DIRECTORY "${toml_f_src_SOURCE_DIR}")
  set_property(DIRECTORY ${toml_f_src_SOURCE_DIR} PROPERTY EXCLUDE_FROM_ALL YES)
endif()

message(STATUS "M_CLI2 source dir: ${m_cli2_src_SOURCE_DIR}")
message(STATUS "toml-f source dir: ${toml_f_src_SOURCE_DIR}")
message(STATUS "fpm source dir: ${fpm_src_SOURCE_DIR}")

# Collect source files
# In general not recommended but fpm has a small footprint and we control the sources
file(GLOB_RECURSE
  SRC_FILES
  ${m_cli2_src_SOURCE_DIR}/src/M_CLI2*.F90
  ${m_cli2_src_SOURCE_DIR}/src/M_CLI2*.f90
  ${toml_f_src_SOURCE_DIR}/src/*.f90
  ${fpm_src_SOURCE_DIR}/src/*.f90
  ${fpm_src_SOURCE_DIR}/src/*.F90
  ${fpm_src_SOURCE_DIR}/src/*.h
  ${fpm_src_SOURCE_DIR}/src/*.c
)

# Make code position independent (-fPIC)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

add_executable(${BIN_NAME} ${SRC_FILES} ${fpm_src_SOURCE_DIR}/app/main.f90)
target_link_libraries(${BIN_NAME} PUBLIC OpenMP::OpenMP_Fortran)

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
