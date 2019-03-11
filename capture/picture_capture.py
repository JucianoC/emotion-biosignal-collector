import os
from datetime import datetime
from multiprocessing import Event
from multiprocessing import Value

import pytz
import cv2

from capture.base_capture import BaseCapture


class PicutureCapture(BaseCapture):

    def __init__(self, interval: float, output_path: str, capture_index: Value,
                 capture_event: Event, terminate_event: Event) -> None:
        self._output_path = output_path
        self._video_capture = cv2.VideoCapture(0)
        super(PicutureCapture, self).__init__(interval, capture_index,
                                              capture_event, terminate_event)

    def start_capture(self) -> None:
        os.makedirs(
            os.path.join(self._output_path,
                         "{:04}".format(self.current_capture)),
            exist_ok=True)
        return super(PicutureCapture, self).start_capture()

    def handler(self) -> None:
        output_image_name = os.path.join(
            self._output_path, "{:04}/capture_{}.png".format(
                self.current_capture,
                pytz.utc.localize(datetime.utcnow()).isoformat()))
        _, frame = self._video_capture.read()
        cv2.imwrite(output_image_name, frame)
