cmake_minimum_required(VERSION 2.4.4)
project(SQLite)

set(INSTALL_BIN_DIR "${CMAKE_INSTALL_PREFIX}/bin" CACHE PATH "Installation directory for executables")
set(INSTALL_LIB_DIR "${CMAKE_INSTALL_PREFIX}/lib" CACHE PATH "Installation directory for libraries")
set(INSTALL_INC_DIR "${CMAKE_INSTALL_PREFIX}/include" CACHE PATH "Installation directory for headers")

set(SQLITE_SRC
sqlite3.h
sqlite3.c
sqlite3ext.h
)

add_library(SQLite3 STATIC ${SQLITE_SRC})
#add_executable(sqlite_main shell.c)
#target_link_libraries(sqlite_main SQLite3)

install(FILES sqlite3.h sqlite3ext.h DESTINATION "${INSTALL_INC_DIR}")

install(TARGETS SQLite3
RUNTIME DESTINATION "${INSTALL_BIN_DIR}"
ARCHIVE DESTINATION "${INSTALL_LIB_DIR}"
LIBRARY DESTINATION "${INSTALL_LIB_DIR}" )
