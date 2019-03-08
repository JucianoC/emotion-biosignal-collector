from __future__ import annotations
import os
import time
from datetime import datetime
from multiprocessing import Process
from multiprocessing import Event

from loguru import logger
import pytz
import cv2


class PicutureCapture:

    def __init__(self, interval: int, output_path: str, capture_event: Event,
                 terminate_event: Event) -> None:
        self._interval = interval
        self._output_path = output_path
        self._video_capture = cv2.VideoCapture(0)
        self._capture_process = None
        self._capture_event = capture_event
        self._terminate_event = terminate_event

    def __enter__(self) -> PicutureCapture:
        self._capture_process = Process(target=self._capture)
        self._capture_process.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._terminate_event.set()
        self._capture_process.join()

    def start_capture(self) -> None:
        assert self._capture_process, "Capture process not started."
        self._capture_event.set()

    def stop_capture(self) -> None:
        assert self._capture_process, "Capture process not started."
        self._capture_event.clear()

    def _capture_and_save_image(self) -> None:
        output_image_name = os.path.join(
            self._output_path, "capture_{}.png".format(
                pytz.utc.localize(datetime.utcnow()).isoformat()))
        _, frame = self._video_capture.read()
        cv2.imwrite(output_image_name, frame)

    def _capture(self) -> None:
        while not self._terminate_event.is_set():
            self._capture_event.wait()
            self._capture_and_save_image()
            time.sleep(self._interval)
