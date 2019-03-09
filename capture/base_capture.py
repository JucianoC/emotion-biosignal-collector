from __future__ import annotations

import time
from abc import ABCMeta
from abc import abstractmethod
from multiprocessing import Process
from multiprocessing import Event
from itertools import count


class BaseCapture(metaclass=ABCMeta):

    def __init__(self, interval: float, capture_event: Event,
                 terminate_event: Event) -> None:
        self._interval = interval
        self._capture_process = None
        self._capture_event = capture_event
        self._terminate_event = terminate_event
        self._capture_count = count(1)
        self._current_capture = 0

    def __enter__(self) -> BaseCapture:
        self._capture_process = Process(target=self._capture)
        self._capture_process.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._terminate_event.set()
        self._capture_event.set()
        self._capture_process.join()

    def start_capture(self) -> None:
        assert self._capture_process, "Capture process not started."
        self._current_capture = next(self._capture_count)
        self._capture_event.set()

    def stop_capture(self) -> None:
        assert self._capture_process, "Capture process not started."
        self._capture_event.clear()

    def _capture(self) -> None:
        while not self._terminate_event.is_set():
            self._capture_event.wait()
            self.handler()
            time.sleep(self._interval)

    @abstractmethod
    def handler(self) -> None:
        ...
