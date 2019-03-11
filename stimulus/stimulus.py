import time
import os
from typing import List
import random
from itertools import count

import cv2
from loguru import logger


class EndOfStimuliSet(BaseException):
    ...


class Stimulus:

    def __init__(self,
                 exposition_period: int,
                 stimulus_path: str,
                 selected_stimulus: List[str] = []) -> None:
        self._stimulus_path = stimulus_path
        self._selected_stimulus = iter(selected_stimulus)
        self._random_stimulus = len(selected_stimulus) == 0
        self._stimulus_exhibited = set()
        self._stimuli = {
            file_name.replace('.jpg', '')
            for file_name in os.listdir(self._stimulus_path)
            if os.path.isfile(os.path.join(self._stimulus_path, file_name)) and
            not file_name.startswith('.') and '.jpg' in file_name
        }
        logger.info(self._stimuli)
        self._stimulus = None
        self._capture_count = count(1)
        self._current_capture = 0
        self._exposition_period = exposition_period
        cv2.namedWindow('stimulus', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('stimulus', cv2.WND_PROP_FULLSCREEN,
                              cv2.WINDOW_FULLSCREEN)

    def __del__(self):
        cv2.destroyWindow('stimulus')

    @property
    def stimulus(self) -> str:
        return self._stimulus

    @stimulus.setter
    def stimulus(self, value: str) -> None:
        self._stimulus = value

    def next_stimulus(self) -> str:
        if self._stimulus_exhibited == self._stimuli:
            raise EndOfStimuliSet("All the stimuli are exhibited.")
        if not self._random_stimulus:
            self.stimulus = next(self._selected_stimulus)
        else:
            self.stimulus = random.choice(
                list(self._stimuli.difference(self._stimulus_exhibited)))
        return os.path.join(self._stimulus_path, "{}.jpg".format(self.stimulus))

    def exhibit_stimulus(self) -> None:
        self._current_capture = next(self._capture_count)
        stimulus_path = self.next_stimulus()
        logger.info(stimulus_path)
        img = cv2.imread(stimulus_path)
        cv2.imshow('stimulus', img)
        cv2.waitKey(self._exposition_period * 1000)
        self._stimulus_exhibited.add(self.stimulus)
