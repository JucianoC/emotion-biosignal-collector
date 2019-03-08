import os
import time
from datetime import datetime

from loguru import logger
import pytz
import cv2


class PicutureCapture:

    def __init__(self, interval, output_path):
        self.interval = interval
        self.output_path = output_path
        self.video_capture = cv2.VideoCapture(0)

    def create_image_output_path(self, capture_datetime):
        return os.path.join(self.output_path, "capture_{}.png".format(capture_datetime.isoformat()))

    def capture(self, collect_event, terminate_event):
        while not terminate_event.is_set():
            collect_event.wait()
            current_datetime = pytz.utc.localize(datetime.utcnow())
            output_image_name = self.create_image_output_path(current_datetime)
            _, frame = self.video_capture.read()
            cv2.imwrite(output_image_name, frame)
            time.sleep(self.interval)
