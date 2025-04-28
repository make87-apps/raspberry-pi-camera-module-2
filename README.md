# Raspberry Pi Camera Module 2

This app captures images from the [Raspberry Pi Camera Module v2](https://www.raspberrypi.com/products/camera-module-v2/) and streams them through the make87 platform. It's designed for Raspberry Pi devices running make87 — no extra setup is needed.

The camera service continuously captures images, compresses them into JPEG format, and publishes them to a messaging topic. It also provides an endpoint where other systems can request the most recent image at any time.

If the camera isn’t available or fails to start, the app will log an error and exit gracefully.

## What It Does
- Captures frames from the Raspberry Pi Camera Module v2 in real-time.
- Encodes each frame as a JPEG image for efficient transmission.
- Publishes images to a `make87` topic called `IMAGE`.
- Offers a `GET_CAMERA_IMAGE` service to fetch the latest captured image on demand.

## Configuration Options
The app automatically reads configuration values from the make87 system:

- **`IMAGE_WIDTH`**  
  Sets the width of captured images. Defaults to 640 pixels.

- **`IMAGE_HEIGHT`**  
  Sets the height of captured images. Defaults to 480 pixels.

- **`IMAGE_FORMAT`**  
  Defines the pixel format for camera output. Defaults to `RGB888`. This must match a format supported by the Picamera2 library.

You can override these values through your make87 configuration if you need a different resolution or format.
