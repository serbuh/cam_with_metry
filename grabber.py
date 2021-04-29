import logging
from grabber_frames import FramesGrabber
from grabber_metry import MetryGrabber

class Grabber():
    def __init__(self, logger):
        self.logger = logger
        self.frames_grabber = FramesGrabber(logger)
        self.metry_grabber = MetryGrabber(logger)

    def grab_loop(self):
        self.metry_grabber.add_listeners()
        self.frames_grabber.grab_frames_loop()

    def exit_grab(self):
        self.metry_grabber.remove_listeners()
    

if __name__ == "__main__":

    # Init logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.info("Welcome to Grabber")

    grabber = Grabber(logger)
    try:
        grabber.grab_loop()
    except KeyboardInterrupt:
        logger.info("Ctrl+C pressed")
        grabber.exit_grab()
