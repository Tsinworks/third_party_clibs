include_directories(
include
src
)

add_library(libusbmuxd STATIC src/libusbmuxd.c)
target_link_libraries(libusbmuxd common_im)

set_target_properties(libusbmuxd PROPERTIES FOLDER "libimobiledevice/lib")