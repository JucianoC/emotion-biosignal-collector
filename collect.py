import time
from multiprocessing import Process
from multiprocessing import Manager

from loguru import logger

from picture_capture import PicutureCapture


class Collect:

    def __init__(self):
        self.picture_capture = PicutureCapture(1, 'captures')

    def run(self):
        with Manager() as manager:
            picture_capture_collect_event = manager.Event()
            picture_capture_terminate_event = manager.Event()
            picture_capture_process = Process(
                target=self.picture_capture.capture,
                args=(picture_capture_collect_event, picture_capture_terminate_event))
            picture_capture_process.start()
            for i in range(5):
                logger.info('Part {}', i)
                picture_capture_collect_event.set()
                time.sleep(10)
                picture_capture_collect_event.clear()
            picture_capture_terminate_event.set()
            picture_capture_process.join()
            logger.info("Process alive: {}", picture_capture_process.is_alive())

if __name__ == '__main__':
    Collect().run()
