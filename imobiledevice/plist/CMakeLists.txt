include_directories(
    include
    src/libcnary/include
    src
)
file(GLOB PLIST_SRCS "src/*.cpp" "src/*.c" "src/*.h" "src/libcnary/*.c")

add_library(plist STATIC ${PLIST_SRCS})

install(TARGETS plist
    RUNTIME DESTINATION bin
    ARCHIVE DESTINATION lib
    LIBRARY DESTINATION lib )
install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/include/plist DESTINATION include)

set_target_properties(plist PROPERTIES FOLDER "libimobiledevice")