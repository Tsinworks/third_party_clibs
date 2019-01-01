cmake_minimum_required(VERSION 3.2)

project(openssl)

option(BUILD_OBJECT_LIBRARY_ONLY "build library only" ON)

include_directories( BEFORE SYSTEM ${CMAKE_CURRENT_BINARY_DIR}/crypto ${CMAKE_CURRENT_BINARY_DIR}/ssl crypto . )
add_definitions(-DOPENSSL_NO_ASM)

if( WIN32 AND NOT CYGWIN )
  add_definitions( -DOPENSSL_SYSNAME_WIN32 )
  add_definitions( -DWIN32_LEAN_AND_MEAN )
endif( )

if( MINGW )
  set( CMAKE_SHARED_LINKER_FLAGS "-Wl,--export-all" )
endif()

add_subdirectory( crypto )
add_subdirectory( ssl )
if( BUILD_OBJECT_LIBRARY_ONLY)
  #file( COPY e_os2.h DESTINATION ${CMAKE_CURRENT_BINARY_DIR} )
else()
  add_subdirectory( apps )

  install( FILES e_os2.h DESTINATION include/openssl )

  install( FILES tools/c_hash tools/c_info tools/c_issuer tools/c_name tools/c_rehash
      FAQ LICENSE PROBLEMS README README.ASN1 README.ENGINE
      DESTINATION share/openssl )

  install( DIRECTORY doc DESTINATION ./ )

  install( FILES e_os2.h DESTINATION include/openssl )

  # Generate the package target
  set( CPACK_GENERATOR ZIP TGZ )
  set( CPACK_PACKAGE_NAME "openssl-cmake" )
  set( CPACK_PACKAGE_VERSION_MAJOR 1  )
  set( CPACK_PACKAGE_VERSION_MINOR 0  )
  set( CPACK_PACKAGE_VERSION_PATCH 1u )

  include( CPack )
endif()