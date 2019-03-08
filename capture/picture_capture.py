import os
from datetime import datetime
from multiprocessing import Event

import pytz
import cv2

from capture.base_capture import BaseCapture


class PicutureCapture(BaseCapture):

    def __init__(self, interval: float, output_path: str, capture_event: Event,
                 terminate_event: Event) -> None:
        self._output_path = output_path
        self._video_capture = cv2.VideoCapture(0)
        super(PicutureCapture, self).__init__(interval, capture_event,
                                              terminate_event)

    def handler(self) -> None:
        output_image_name = os.path.join(
            self._output_path, "capture_{}.png".format(
                pytz.utc.localize(datetime.utcnow()).isoformat()))
        _, frame = self._video_capture.read()
        cv2.imwrite(output_image_name, frame)
