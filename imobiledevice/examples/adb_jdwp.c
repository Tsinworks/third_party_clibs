#include <libimobiledevice/adb.h>

void device_list_running_process(const char* udid)
{
    if (!udid)
        return;
    idevice_t device;
    idevice_new(&device, udid);
    if (idevice_get_type(device) == IDEVICE_ANDROID) {
        adb_client_t adb_client;
        adb_client_new(&adb_client, device);
        //adb_client_subscribe_()
        adb_client_free(adb_client);
    }
    idevice_free(device);
}

void device_callback(const idevice_event_t *event, void *user_data)
{
    switch (event->event)
    {
    case IDEVICE_DEVICE_ADD:
    {
        printf("device %s online.\n", event->udid);
        device_list_running_process(event->udid);
        break;
    }
    case IDEVICE_DEVICE_REMOVE:
        printf("device %s offline.\n", event->udid);
        break;
    }
}

int main(int argc, char ** argv)
{
    idevice_event_subscribe(device_callback, NULL);
    while (1);
    return 0;
}