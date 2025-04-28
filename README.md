# Raspberry Pi Camera Module 2

This app connects and streams images from the [Raspberry Pi Camera Module v2](https://www.raspberrypi.com/products/camera-module-v2/) using the make87 framework. It continuously captures frames from the Pi Camera, encodes them in JPEG format, and publishes them over a `make87` messaging topic. It also provides an endpoint for clients to request the latest available image at any time.

The camera uses the Raspberry Pi's Picamera2 library, and this service is intended to run on systems managed by make87 without additional setup requirements.

## Functionality
- **Continuous Image Capture:** Captures frames from the Raspberry Pi Camera Module v2.
- **JPEG Encoding:** Frames are automatically converted into JPEG format for efficient transmission.
- **Realtime Publishing:** Publishes each JPEG image to the `IMAGE` topic within the make87 platform.
- **On-Demand Retrieval:** Provides the latest captured image through a `GET_CAMERA_IMAGE` service endpoint.

If the camera cannot be initialized (e.g., not connected or permissions issue), the app will log an error and stop.

## Configuration Values
This app reads the following configuration values from the make87 environment:

| Config Key     | Default | Description                                                                 |
|----------------|---------|-----------------------------------------------------------------------------|
| `IMAGE_WIDTH`  | 640     | Width of the captured image in pixels.                                       |
| `IMAGE_HEIGHT` | 480     | Height of the captured image in pixels.                                      |
| `IMAGE_FORMAT` | `RGB888`| Pixel format used by the camera (must match supported formats of Picamera2). |

Changing these values allows you to adjust the resolution and internal format of the captured images depending on your needs.
