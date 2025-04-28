import threading
from threading import Thread
import logging
import numpy as np
import cv2

from make87_messages.core.empty_pb2 import Empty
from make87_messages.core.header_pb2 import Header
from make87_messages.image.compressed.image_jpeg_pb2 import ImageJPEG

import make87
from picamera2.picamera2 import Picamera2


class Camera:
    def __init__(self, img_width: int, img_height: int, format: str = "RGB888"):
        self.img_width = img_width
        self.img_height = img_height
        self.format = format
        self.last_image_lock = threading.Lock()
        self.last_image = None


    def handle_get_latest_camera_image(self, request: Empty) -> ImageJPEG:
        # This method is not implemented in the original code
        # You can implement it if needed
        img_msg = None
        with self.last_image_lock:
            if self.last_image is not None:
                img_msg = self.last_image
            else:
                header = make87.create_header(Header, entity_path="/picamera")
                img_msg = ImageJPEG(data=b"", header=header)

        return img_msg

    def publish_camera_image(self):
        topic = make87.get_publisher(name="IMAGE", message_type=ImageJPEG)

        try:
            picam2 = Picamera2()
            video_config = picam2.create_video_configuration(
                main={"size": (self.img_width, self.img_height), "format": self.format}
            )
            picam2.configure(video_config)
            picam2.start()
        except Exception as e:
            logging.error(f"Cannot initialize camera: {e}")
            return

        while True:
            try:
                frame = picam2.capture_array()
                ret, frame_jpeg = cv2.imencode(".jpeg", frame)
                if not ret:
                    logging.error("Error: Could not encode frame to JPEG.")
                    break
                frame_jpeg_bytes = frame_jpeg.tobytes()
                header = make87.create_header(Header, entity_path="/picamera")
                message = ImageJPEG(data=frame_jpeg_bytes, header=header)
                with self.last_image_lock:
                    self.last_image = message
                topic.publish(message)
            except Exception as e:
                logging.error(f"Error while capturing or publishing image: {e}")
                break

        picam2.stop()

    def run(self):
        camera_thread = Thread(target=self.publish_camera_image)
        camera_thread.start()

        camera_image_endpoint = make87.get_provider(
            name="GET_CAMERA_IMAGE",
            requester_message_type=Empty,
            provider_message_type=ImageJPEG,
        )
        camera_image_endpoint.provide(self.handle_get_latest_camera_image)

        camera_thread.join()


def main():
    make87.initialize()
    image_width = make87.get_config_value("IMAGE_WIDTH", 640)
    image_height = make87.get_config_value("IMAGE_HEIGHT", 480)
    image_format = make87.get_config_value("IMAGE_FORMAT", "RGB888")
    cam = Camera(img_width=image_width, img_height=image_height, format=image_format)
    cam.run()


if __name__ == "__main__":
    main()
