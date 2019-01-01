include_directories(.)
include_directories(common)
include_directories(libusbmuxd/include)

add_subdirectory(common)
add_subdirectory(libusbmuxd)

add_library(libimobiledevice SHARED
iadb.c
afc.c
debugserver.c
device_link_service.c
diagnostics_relay.c
file_relay.c
heartbeat.c
house_arrest.c
idevice.c
installation_proxy.c
lockdown.c
misagent.c
mobile_image_mounter.c
mobileactivation.c
mobilebackup.c
mobilebackup2.c
mobilesync.c
notification_proxy.c
pinvoke.c
property_list_service.c
restore.c
sbservices.c
screenshotr.c
service.c
syslog_relay.c
webinspector.c
)
target_link_libraries(libimobiledevice common_im libusbmuxd plist ${OPENSSL_SSL_LIBRARY} ${OPENSSL_CRYPTO_LIBRARY} ${ZLIB_LIBRARY})
target_include_directories(libimobiledevice PRIVATE "${OPENSSL_INCLUDE_DIR}")
target_compile_definitions(libimobiledevice PRIVATE HAVE_OPENSSL=1)
set_target_properties(libimobiledevice PROPERTIES FOLDER "libimobiledevice/lib")

if(WIN32)
    target_link_libraries(libimobiledevice Crypt32.lib)
endif()

install(TARGETS libimobiledevice
    RUNTIME DESTINATION bin
    ARCHIVE DESTINATION lib
    LIBRARY DESTINATION lib )