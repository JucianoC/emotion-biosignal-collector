import os
import sys
import time
import json
from multiprocessing import Process
from multiprocessing import Manager

import dotenv
import cv2
from loguru import logger

from capture.picture_capture import PicutureCapture
from capture.signal_capture import SignalCapture
from stimulus_manager.stimulus import Stimulus
from stimulus_manager.self_assessment_manikin import SelfAssessmentManikin
from serializer import Serializer


def load_env():
    dotenv.load_dotenv()
    missing_keys = {
        "EBC_PICTURE_CAPTURE_OUTPUT_PATH", "EBC_SIGNAL_PORT",
        "EBC_STIMULUS_IAPS_PATH", "EBC_SUBJECT_ID", "EBC_SESSION_ID"
    }.difference(set(os.environ.keys()))
    assert not missing_keys, "You shold define the following environment variables: {}".format(
        missing_keys)
    os.environ.update({
        'EBC_PICTURE_CAPTURE_INTERVAL':
        os.getenv("EBC_PICTURE_CAPTURE_INTERVAL", "1"),
        'EBC_SIGNAL_BOUND_RATE':
        os.getenv("EBC_SIGNAL_BOUND_RATE", "9600"),
        'EBC_STIMULUS_EXHIBITION_TIME':
        os.getenv("EBC_STIMULUS_EXHIBITION_TIME", "10"),
    })


class Collect:

    def __init__(self):
        cv2.namedWindow('stimulus', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('stimulus', cv2.WND_PROP_FULLSCREEN,
                              cv2.WINDOW_FULLSCREEN)
        self.serializer = Serializer(
            int(os.getenv("EBC_SUBJECT_ID")), int(os.getenv("EBC_SESSION_ID")))

    def __del__(self):
        cv2.destroyWindow('stimulus')

    def run(self):
        with Manager() as manager:
            capture_index = manager.Value(int, value=0)
            with PicutureCapture(
                    float(os.getenv("EBC_PICTURE_CAPTURE_INTERVAL")),
                    os.getenv("EBC_PICTURE_CAPTURE_OUTPUT_PATH"), capture_index,
                    manager.Event(), manager.Event()) as picture_capture:
                with SignalCapture(
                        os.getenv("EBC_SIGNAL_PORT"),
                        float(os.getenv("EBC_SIGNAL_BOUND_RATE")),
                        manager.list(), 0, capture_index, manager.Event(),
                        manager.Event()) as signal_capture:
                    stimulus = Stimulus(
                        int(os.getenv("EBC_STIMULUS_EXPOSITION_PERIOD")),
                        os.getenv("EBC_STIMULUS_IAPS_PATH"))
                    sam = SelfAssessmentManikin(
                        int(os.getenv('EBC_SAM_TIME_LIMIT', "15")))
                    for i in range(5):
                        capture_index.value = i
                        logger.info('Capture {:04}', i)
                        signal_capture.start_capture()
                        picture_capture.start_capture()
                        stimulus.exhibit_stimulus()
                        picture_capture.stop_capture()
                        signal_capture.stop_capture()
                        signals = signal_capture.pop_buffer()
                        try:
                            sam.apply_test()
                        except ValueError:
                            logger.warning(
                                "Incorrect response in SAM, missed capture {:04}",
                                capture_index.value)
                        # time.sleep(10)
                        logger.info("{:03} Singals: {}", len(signals), signals)
                        logger.info("Valence: {} | Arousal: {}", sam.valence,
                                    sam.arousal)
                        self.serializer.serialize(
                            capture_index.value, stimulus.stimulus, sam.valence,
                            sam.arousal, signals)
            logger.info("Picture alive: {}",
                        picture_capture._capture_process.is_alive())
            logger.info("Signal alive: {}",
                        signal_capture._capture_process.is_alive())


if __name__ == '__main__':
    logger.remove()
    logger.add(
        sys.stdout,
        format="<g>{time}</g> | <lvl>{level}</lvl> | <lvl>{message}</lvl>")
    load_env()
    Collect().run()
