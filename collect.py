import sys
import time
from multiprocessing import Process
from multiprocessing import Manager

from loguru import logger
logger.remove()
logger.add(
    sys.stdout,
    format="<g>{time}</g> | <lvl>{level}</lvl> | <lvl>{message}</lvl>")

from capture.picture_capture import PicutureCapture
from capture.signal_capture import SignalCapture


class Collect:

    def run(self):
        with Manager() as manager:
            with PicutureCapture(1, 'collects', manager.Event(),
                                 manager.Event()) as picture_capture:
                with SignalCapture('/dev/ttyACM0', 9600, manager.list(), 0,
                                   manager.Event(),
                                   manager.Event()) as signal_capture:
                    for i in range(5):
                        logger.info('Part {}', i)
                        signal_capture.start_capture()
                        picture_capture.start_capture()
                        time.sleep(3)
                        picture_capture.stop_capture()
                        signal_capture.stop_capture()
                        signals = signal_capture.pop_buffer()
                        logger.info("{:03} Singals: {}", len(signals), signals)
            logger.info("Picture alive: {}",
                        picture_capture._capture_process.is_alive())
            logger.info("Signal alive: {}",
                        signal_capture._capture_process.is_alive())


if __name__ == '__main__':
    Collect().run()
