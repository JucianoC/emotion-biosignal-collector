import os
import time
from datetime import datetime
from multiprocessing import Process

from loguru import logger
import pytz
import cv2


class PicutureCapture:

    def __init__(self,
                 interval,
                 output_path,
                 capture_event=None,
                 terminate_event=None):
        self.interval = interval
        self.output_path = output_path
        self.video_capture = cv2.VideoCapture(0)
        self.capture_process = None
        self._capture_event = capture_event
        self._terminate_event = terminate_event

    @property
    def capture_event(self):
        return self._capture_event

    @property
    def terminate_event(self):
        return self._terminate_event

    @capture_event.setter
    def capture_event(self, event):
        self._capture_event = event

    @terminate_event.setter
    def terminate_event(self, event):
        self._terminate_event = event

    def __enter__(self):
        assert self.capture_event and self.terminate_event, "Flow control events must be setted"
        self.capture_process = Process(
            target=self._capture_process,
            args=(self.capture_event, self.terminate_event))
        self.capture_process.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.terminate_event.set()
        self.capture_process.join()

    def start_capture(self):
        assert self.capture_process, "Capture process not started."
        self.capture_event.set()

    def stop_capture(self):
        assert self.capture_process, "Capture process not started."
        self.capture_event.clear()

    def _capture_and_save_image(self):
        output_image_name = os.path.join(
            self.output_path, "capture_{}.png".format(
                pytz.utc.localize(datetime.utcnow()).isoformat()))
        _, frame = self.video_capture.read()
        cv2.imwrite(output_image_name, frame)

    def _capture_process(self, capture_event, terminate_event):
        while not terminate_event.is_set():
            capture_event.wait()
            self._capture_and_save_image()
            time.sleep(self.interval)
