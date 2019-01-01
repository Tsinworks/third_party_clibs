cmake_minimum_required(VERSION 3.2)

project(ThirdPartyCLibs)

option(BUILD_WITH_OPTIONAL_LIBS "optional libs" OFF)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${ThirdPartyCLibs_SOURCE_DIR}/bin/")

foreach(OUTPUTCONFIG ${CMAKE_CONFIGURATION_TYPES})
    string(TOUPPER ${OUTPUTCONFIG} OUTPUTCONFIG)
    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_${OUTPUTCONFIG} ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
endforeach(OUTPUTCONFIG CMAKE_CONFIGURATION_TYPES)

if (MSVC)
    add_definitions(/MP)
endif()

if(${CMAKE_SYSTEM_NAME} STREQUAL "WindowsStore")
    add_definitions(/ZW)
endif()

add_subdirectory(freetype-2.7)

if(BUILD_WITH_OPTIONAL_LIBS)
	add_subdirectory(pcre2)
    add_subdirectory(sqlite3)
endif()

if(WIN32) # Linux Or Mac
    add_subdirectory(imobiledevice)
endif()
install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/vulkan DESTINATION include)