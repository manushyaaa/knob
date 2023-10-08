import pywinusb.hid as hid
import time

# Define the VID and PID of the USB device you want to monitor
target_vid = 0x1a86  # Replace with your desired VID
target_pid = 0x7523  # Replace with your desired PID

# Function to check if a device matches the target VID and PID
def is_target_device(device):
    return device.vendor_id == target_vid and device.product_id == target_pid

# Create an event handler for device insertion
def on_device_inserted(data):
    device = data.device
    if is_target_device(device):
        print(f"USB device inserted - VID:{device.vendor_id}, PID:{device.product_id}")

# Create an event handler for device removal
def on_device_removed(data):
    device = data.device
    if is_target_device(device):
        print(f"USB device removed - VID:{device.vendor_id}, PID:{device.product_id}")

# Find all HID devices
all_devices = hid.HidDeviceFilter().get_devices()

# Filter and monitor only the target device
target_devices = [device for device in all_devices if is_target_device(device)]

if not target_devices:
    print(f"No USB devices with VID:{target_vid} and PID:{target_pid} found.")
else:
    print(f"Monitoring USB devices with VID:{target_vid} and PID:{target_pid}...")

    for device in target_devices:
        device.open()
        device.set_raw_data_handler(on_device_inserted)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for device in target_devices:
            device.close()


"""In the "Property" dropdown, select "Hardware Ids."
 You will see a list of values in the "Value" box.
  The VID and PID are part of these values and are typically in the 
  format VID_xxxx&PID_xxxx,
 where xxxx represents the four-digit hexadecimal VID and PID values.

 usb\vid_1a86&pid_7523

"""
