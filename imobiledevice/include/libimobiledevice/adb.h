/*
* adb.h
* Device discovery and communication interface -- header file.
*
* Copyright (c) 2018 Zhou Qin. All Rights Reserved.
*
* This library is free software; you can redistribute it and/or
* modify it under the terms of the GNU Lesser General Public
* License as published by the Free Software Foundation; either
* version 2.1 of the License, or (at your option) any later version.
*
* This library is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
* Lesser General Public License for more details.
*
* You should have received a copy of the GNU Lesser General Public
* License along with this library; if not, write to the Free Software
* Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
*/

#ifndef IMOBILEDEVICE_ADB_H
#define IMOBILEDEVICE_ADB_H

#ifdef __cplusplus
extern "C" {
#endif

#include <libimobiledevice/libimobiledevice.h>

typedef enum {
    ADB_CLIENT_E_SUCCESS = 0,
    ADB_CLIENT_E_SEND_REQUEST_FAILED = -1,
    ADB_CLIENT_E_RESPONSE_FAILED = -2,
    ADB_CLIENT_E_RECV_RESPONSE_FAILED = -3,
} adb_client_error_t;

typedef struct adb_client_private adb_client_private;
typedef adb_client_private *adb_client_t;

LIBIMOBILEDEVICE_API_MSC adb_client_error_t adb_client_new(adb_client_t *client, idevice_t device);
LIBIMOBILEDEVICE_API_MSC adb_client_error_t adb_client_free(adb_client_t client);
LIBIMOBILEDEVICE_API_MSC adb_client_error_t adb_client_get_device_name(adb_client_t client, char **device_name);
LIBIMOBILEDEVICE_API_MSC adb_client_error_t adb_client_get_device_prop(adb_client_t client, const char *key, char**value);

typedef struct jdwp_client_private jdwp_client_private;
typedef jdwp_client_private *jdwp_client_t;

typedef enum {
    ADB_JDWP_PROCESS_ADD,
    ADB_JDWP_PROCESS_DEAD
} adb_jdwp_event_type;

typedef struct {
    idevice_t device;
    enum adb_jdwp_event_type type;
    int pid; // process id
} adb_jdwp_event_t;
typedef void(*adb_jdwp_event_cb_t) (const adb_jdwp_event_t *event, void *user_data);

// jdwp
LIBIMOBILEDEVICE_API_MSC adb_client_error_t adb_client_jdwp_subscribe(adb_client_t client, adb_jdwp_event_cb_t callback, void* data);
LIBIMOBILEDEVICE_API_MSC adb_client_error_t adb_client_jdwp_unsubscribe(adb_client_t client);

LIBIMOBILEDEVICE_API_MSC void jdwp_client_new(jdwp_client_t * jdwp, adb_client_t adb_device_client);
LIBIMOBILEDEVICE_API_MSC void jdwp_client_free(jdwp_client_t jdwp);

#ifdef __cplusplus
}
#endif
#endif