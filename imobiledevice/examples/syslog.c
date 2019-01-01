#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#ifdef _MSC_VER
//#include <config_msvc.h>
#endif

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <libimobiledevice/libimobiledevice.h>
#include <libimobiledevice/adb.h>
#include <libimobiledevice/syslog_relay.h>

void cb(char c, void *data)
{
    putchar(c);
}

int main(int argc, char **argv)
{
    idevice_t device = NULL;
    char **dev_list = NULL;
    char *device_name = NULL;
    int count = 0;
    idevice_get_device_list(&dev_list, &count);
    if (count > 0) {
        idevice_new(&device, dev_list[0]);

        syslog_relay_client_t syslog = NULL;
        syslog_relay_error_t serr = SYSLOG_RELAY_E_UNKNOWN_ERROR;
        serr = syslog_relay_client_start_service(device, &syslog, "idevicesyslog");
        serr = syslog_relay_start_capture(syslog, cb, NULL);
        if (serr != SYSLOG_RELAY_E_SUCCESS) {
            fprintf(stderr, "ERROR: Unable tot start capturing syslog.\n");
            syslog_relay_client_free(syslog);
            syslog = NULL;
            return -1;
        }
        while (1);
        idevice_free(device);
    }
    idevice_device_list_free(dev_list);
}