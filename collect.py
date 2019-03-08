import time
from multiprocessing import Process
from multiprocessing import Manager

from loguru import logger

from picture_capture import PicutureCapture


class Collect:

    def run(self):
        with Manager() as manager:
            with PicutureCapture(1, 'captures', manager.Event(),
                                 manager.Event()) as picture_capture:
                for i in range(5):
                    logger.info('Part {}', i)
                    picture_capture.start_capture()
                    time.sleep(3)
                    picture_capture.stop_capture()

            logger.info("Process alive: {}",
                        picture_capture._capture_process.is_alive())


if __name__ == '__main__':
    Collect().run()
