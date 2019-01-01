
set(ZIP_SRC
zip.h zip.c
unzip.h unzip.c
crypt.h
)
list(APPEND ZIP_SRC ioapi.c)

if(WIN32)
list(APPEND ZIP_SRC iowin32.c)
endif()

source_group(zip FILES ${ZIP_SRC})
add_library(libzip ${ZIP_SRC})

add_executable(miniunz miniunz.c)
target_link_libraries(miniunz libzip zlib)
add_executable(minizip minizip.c)
target_link_libraries(minizip libzip zlib)

set(LIBZIP_PUBLIC_HDRS zip.h unzip.h ioapi.h)

if(NOT SKIP_INSTALL_LIBRARIES AND NOT SKIP_INSTALL_ALL )
    install(TARGETS libzip minizip miniunz
        RUNTIME DESTINATION "${INSTALL_BIN_DIR}"
        ARCHIVE DESTINATION "${INSTALL_LIB_DIR}"
        LIBRARY DESTINATION "${INSTALL_LIB_DIR}" )
endif()
if(NOT SKIP_INSTALL_HEADERS AND NOT SKIP_INSTALL_ALL )
    install(FILES ${LIBZIP_PUBLIC_HDRS} DESTINATION "${INSTALL_INC_DIR}")
endif()