import pyrealsense2 as rs
import sys

# Enable internal logging to console
rs.log_to_console(rs.log_severity.debug)

# Version check removed (caused AttributeError on embedded libs)

print("[Debug] Checking RealSense Context...")
ctx = rs.context()
devices = ctx.query_devices()
dev_count = len(devices)

print(f"[Debug] Devices found in context: {dev_count}")

if dev_count == 0:
    print("[Error] No devices found via pyrealsense2, despite lsusb detecting it.")
    print("Possibilities:")
    print(" 1. Missing UDEV rules (/etc/udev/rules.d/99-realsense-libusb.rules)")
    print(" 2. Kernel driver (uvcvideo) issues.")
    sys.exit(1)

for i, dev in enumerate(devices):
    name = dev.get_info(rs.camera_info.name)
    serial = dev.get_info(rs.camera_info.serial_number)
    usb_type = dev.get_info(rs.camera_info.usb_type_descriptor)
    print(f"\n[Device {i}]")
    print(f"  Name: {name}")
    print(f"  Serial: {serial}")
    print(f"  USB Type detected: {usb_type}")
    
    if "2.1" in usb_type or "2.0" in usb_type:
        print("[Warning] Camera is connected via USB 2.0!")
        print("          High resolutions and FPS will NOT work.")
        print("          Please use a USB 3.0 (SS) cable and port.")

# Try a minimal config test
print("\n[Debug] Attempting minimal config (USB2 friendly)...")
pipeline = rs.pipeline()
config = rs.config()
# Low res, low fps should work on USB2
config.enable_stream(rs.stream.depth, 480, 270, rs.format.z16, 15)
config.enable_stream(rs.stream.color, 424, 240, rs.format.bgr8, 15)

try:
    pipeline.start(config)
    print("[Success] Pipeline started with minimal config!")
    pipeline.stop()
except Exception as e:
    print(f"[Error] Pipeline failed to start: {e}")
