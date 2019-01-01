#include <libimobiledevice/libimobiledevice.h>
#include <libimobiledevice/adb.h>

void device_callback(const idevice_event_t *event, void *user_data)
{
    switch (event->event)
    {
    case IDEVICE_DEVICE_ADD:
        printf("device %s online.\n", event->udid);
        break;
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