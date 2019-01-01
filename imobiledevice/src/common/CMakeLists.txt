include_directories(.)

set(COMMON_SRC
collection.c
debug.c
libgen.c
socket.c
userpref.c
utils.c
thread.c
)

add_library(common_im STATIC ${COMMON_SRC})
target_include_directories(common_im PRIVATE ${OPENSSL_INCLUDE_DIR})
target_compile_definitions(common_im PRIVATE HAVE_OPENSSL=1)
set_target_properties(common_im PROPERTIES FOLDER "libimobiledevice/lib")