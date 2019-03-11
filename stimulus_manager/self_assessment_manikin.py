import os

import cv2


class SelfAssessmentManikin:

    def __init__(self, time_limit: int) -> None:
        self._time_limit = time_limit
        self.valence = 0
        self.arousal = 0
        self._valence_img = cv2.imread(os.path.join("sam", "valence.png"))
        self._arousal_img = cv2.imread(os.path.join("sam", "arousal.png"))

    def apply_test(self) -> None:
        cv2.imshow('stimulus', self._valence_img)
        valence_key = cv2.waitKey(self._time_limit * 500)
        cv2.imshow('stimulus', self._arousal_img)
        arousal_key = cv2.waitKey(self._time_limit * 500)
        acceptable_keys = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
        if chr(valence_key) not in acceptable_keys or chr(
                arousal_key) not in acceptable_keys:
            raise ValueError("Some not acceptable key was typed.")
        self.valence = int(chr(valence_key))
        self.arousal = int(chr(arousal_key))
