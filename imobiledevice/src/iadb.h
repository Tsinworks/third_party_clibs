/*
* iadb.h
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

#ifndef __IADB_H
#define __IADB_H
#include "libimobiledevice/adb.h"
#include "idevice.h"

struct adb_client_private
{
    idevice_t   device;
    char        name[64];       //ro.product.model
    char        os_version[16]; //ro.build.version.release
    int         sdk_version;    //ro.build.version.sdk
};

struct jdwp_client_private
{
    idevice_connection_private* conn;
    int         pid;
    char        pname[128];
};

extern adb_client_error_t adb_connection_send_request(idevice_connection_t connection, const char* request);
extern adb_client_error_t adb_connection_read_response(idevice_connection_t connection, int* succeed, char** msg);


#endif