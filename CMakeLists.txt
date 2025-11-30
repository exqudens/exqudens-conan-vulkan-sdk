cmake_minimum_required(VERSION "3.25" FATAL_ERROR)

message(STATUS "CMAKE_COMMAND: '${CMAKE_COMMAND}'")
message(STATUS "CMAKE_VERSION: '${CMAKE_VERSION}'")
message(STATUS "PRESET_NAME: '${PRESET_NAME}'")

string(REPLACE "." ";" PRESET_NAME_ELEMENTS "${PRESET_NAME}")
set(USE_CONAN "1" CACHE BOOL "...")

message(STATUS "USE_CONAN: '${USE_CONAN}'")

if("${USE_CONAN}")
    find_program(CONAN_COMMAND NAMES "conan.exe" "conan" PATHS ENV CONAN_PATH ENV PATH REQUIRED NO_CACHE NO_DEFAULT_PATH)
endif()

file(READ "${CMAKE_CURRENT_SOURCE_DIR}/name-version.json" NAME_VERSION_JSON)
string(JSON NAME GET "${NAME_VERSION_JSON}" "name")
string(JSON VERSION GET "${NAME_VERSION_JSON}" "version")
project("${NAME}" VERSION "${VERSION}" LANGUAGES "NONE")

message(STATUS "PROJECT_NAME: '${PROJECT_NAME}'")
message(STATUS "PROJECT_VERSION: '${PROJECT_VERSION}'")
message(STATUS "PROJECT_SOURCE_DIR: '${PROJECT_SOURCE_DIR}'")
message(STATUS "PROJECT_BINARY_DIR: '${PROJECT_BINARY_DIR}'")

set(CMAKE_INSTALL_PREFIX "${CMAKE_BINARY_DIR}/cmake-install" CACHE PATH "..." FORCE)

message(STATUS "CMAKE_INSTALL_PREFIX: '${CMAKE_INSTALL_PREFIX}'")

if("windows" IN_LIST "PRESET_NAME_ELEMENTS" AND "${TARGET_DIR}" STREQUAL "")
    set(INSTALL_PREFIX_LIB_DIR_NAME "Lib")
else()
    set(INSTALL_PREFIX_LIB_DIR_NAME "lib")
endif()

set(TARGET_DIR "" CACHE STRING "...")

if("windows" IN_LIST "PRESET_NAME_ELEMENTS" AND "${TARGET_DIR}" STREQUAL "")
    set(TARGET_DIR "C:/VulkanSDK/${PROJECT_VERSION}" CACHE STRING "..." FORCE)
endif()

message(STATUS "TARGET_DIR: '${TARGET_DIR}'")

if("${TARGET_DIR}" STREQUAL "")
    message(FATAL_ERROR "'TARGET_DIR' is empty")
endif()

include("CMakePackageConfigHelpers")
configure_package_config_file(
    "${PROJECT_SOURCE_DIR}/package-config.cmake.in"
    "${PROJECT_BINARY_DIR}/${PROJECT_NAME}-config.cmake"
    INSTALL_DESTINATION "${INSTALL_PREFIX_LIB_DIR_NAME}/cmake/${PROJECT_NAME}"
)
write_basic_package_version_file(
    "${PROJECT_BINARY_DIR}/${PROJECT_NAME}-config-version.cmake"
    VERSION "${PROJECT_VERSION}"
    COMPATIBILITY "ExactVersion"
)
install(
    DIRECTORY "${TARGET_DIR}/"
    DESTINATION "."
    FILES_MATCHING
    PATTERN "*.*"
)
install(
    FILES "${PROJECT_BINARY_DIR}/${PROJECT_NAME}-config.cmake"
          "${PROJECT_BINARY_DIR}/${PROJECT_NAME}-config-version.cmake"
    DESTINATION "${INSTALL_PREFIX_LIB_DIR_NAME}/cmake/${PROJECT_NAME}"
)

add_custom_command(
    OUTPUT "${CMAKE_INSTALL_PREFIX}/${INSTALL_PREFIX_LIB_DIR_NAME}/cmake/${PROJECT_NAME}/${PROJECT_NAME}-config.cmake"
    COMMAND "${CMAKE_COMMAND}" "--install" "${PROJECT_BINARY_DIR}" "--prefix" "${CMAKE_INSTALL_PREFIX}"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    USES_TERMINAL
    VERBATIM
)

add_custom_target("cmake-install" ALL
    DEPENDS "${CMAKE_INSTALL_PREFIX}/${INSTALL_PREFIX_LIB_DIR_NAME}/cmake/${PROJECT_NAME}/${PROJECT_NAME}-config.cmake"
)

if("${USE_CONAN}")
    add_custom_target("conan-export"
        COMMAND "${CONAN_COMMAND}" "export-pkg"
                "--output-folder" "${CMAKE_INSTALL_PREFIX}"
                #"--user" "gitlab-group+gitlab-sub-group+${PROJECT_NAME}"
                #"--channel" "stable"
                "${PROJECT_SOURCE_DIR}/conanfile.py"
        DEPENDS "cmake-install"
        WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
        USES_TERMINAL
        VERBATIM
    )

    add_custom_target("conan-remove"
        COMMAND "${CONAN_COMMAND}" "remove" "-c" "${PROJECT_NAME}/${PROJECT_VERSION}"
        WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
        USES_TERMINAL
        VERBATIM
    )

    add_custom_target("conan-list"
        COMMAND "${CONAN_COMMAND}" "list" "${PROJECT_NAME}/${PROJECT_VERSION}:*"
        WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
        USES_TERMINAL
        VERBATIM
    )
endif()

set("${PROJECT_NAME}_ADDITIONAL_CLEAN_FILES"
    "${CMAKE_INSTALL_PREFIX}"
)
set_directory_properties(PROPERTIES
    ADDITIONAL_CLEAN_FILES "${${PROJECT_NAME}_ADDITIONAL_CLEAN_FILES}"
)
