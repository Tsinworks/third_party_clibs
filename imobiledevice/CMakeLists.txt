cmake_minimum_required(VERSION 3.2)
set_property(GLOBAL PROPERTY USE_FOLDERS ON)
project(imobiledevice)

if (${CMAKE_CXX_COMPILER_ID} STREQUAL "MSVC")
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /MP")
endif()

include_directories(.)
include_directories(include)
include_directories(plist/include)
include_directories(src/libusbmuxd/include)
include_directories(src/common)

add_subdirectory(plist)
add_subdirectory(src)
add_subdirectory(examples)

install(DIRECTORY include/libimobiledevice DESTINATION include)