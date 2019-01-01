#include "iadb.h"
#include "socket.h"
#include <string.h>
#include <stdio.h>
#include <usbmuxd.h>
#include "common/debug.h"

#define ADB_REQ_BUF_SZ 128

adb_client_error_t adb_connection_read_response(idevice_connection_t connection, int* succeed, char** msg)
{
    *msg = NULL;
    char buffer[5] = { 0 };
    uint32_t recv_bytes = 0;
    idevice_connection_receive(connection, buffer, 4, &recv_bytes);
    if (recv_bytes < 4)
        return ADB_CLIENT_E_RECV_RESPONSE_FAILED;
    if (strncmp(buffer, "OKAY", 4)) {
        uint32_t payload = 0;
        idevice_connection_receive(connection, (char*)&payload, 4, &recv_bytes);
        if (recv_bytes < 4)
            return ADB_CLIENT_E_RECV_RESPONSE_FAILED;
        if (msg) {
            *msg = (char*)malloc(payload + 1);
            msg[payload] = '\0';
            idevice_connection_receive(connection, msg, payload, &recv_bytes);
            if (recv_bytes < payload) {
                return ADB_CLIENT_E_RECV_RESPONSE_FAILED;
            }
        }
    }
    return ADB_CLIENT_E_SUCCESS;
}

adb_client_error_t adb_connection_send_request(idevice_connection_t connection, const char* request)
{
    uint32_t strreq_len = (uint32_t)strlen(request);
    uint32_t req_len = strreq_len + 4;
    uint32_t sent_bytes = 0;
    enum idevice_error_t ret;
    if (req_len> ADB_REQ_BUF_SZ) {
        char* newbuffer = (char*)malloc(req_len + 1);
        snprintf(newbuffer, req_len + 1, "%04x%s", strreq_len, request);
        ret = idevice_connection_send(connection, newbuffer, req_len, &sent_bytes);
        free(newbuffer);
    }
    else {
        char tmpbuffer[ADB_REQ_BUF_SZ] = { 0 };
        snprintf(tmpbuffer, 1024, "%04x%s", strreq_len, request);
        ret = idevice_connection_send(connection, tmpbuffer, req_len, &sent_bytes);
    }
    if (sent_bytes < req_len) {
        return ADB_CLIENT_E_SEND_REQUEST_FAILED;
    }
    char * msg = NULL;
    int succeed = 0;
    adb_connection_read_response(connection, &succeed, &msg);
    debug_info("ERROR: send adb request (%s) failed, %s.", request, msg);
    if (!succeed && msg) {
        free(msg);
    }
    return ADB_CLIENT_E_SUCCESS;
}

LIBIMOBILEDEVICE_API adb_client_error_t adb_client_new(adb_client_t *client, idevice_t device)
{
    return ADB_CLIENT_E_SUCCESS;
}

LIBIMOBILEDEVICE_API adb_client_error_t adb_client_free(adb_client_t client)
{
    return ADB_CLIENT_E_SUCCESS;
}

LIBIMOBILEDEVICE_API adb_client_error_t adb_client_get_device_name(adb_client_t client, char **device_name)
{
    return ADB_CLIENT_E_SUCCESS;
}

LIBIMOBILEDEVICE_API adb_client_error_t adb_client_get_device_prop(adb_client_t client, const char *key, char**value)
{
    return ADB_CLIENT_E_SUCCESS;
}

LIBIMOBILEDEVICE_API adb_client_error_t adb_client_jdwp_subscribe(adb_client_t client, adb_jdwp_event_cb_t callback, void* data)
{
    return ADB_CLIENT_E_SUCCESS;
}

LIBIMOBILEDEVICE_API adb_client_error_t adb_client_jdwp_unsubscribe(adb_client_t client)
{
    return ADB_CLIENT_E_SUCCESS;
}