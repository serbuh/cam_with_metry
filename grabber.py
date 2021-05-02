import logging
from grabber_frames import FramesGrabber
from grabber_metry import MetryGrabber
import cv2

class Grabber():
    def __init__(self, logger):
        self.logger = logger
        
        # Init frames grabber
        self.frames_grabber = FramesGrabber(logger, "Video         ")
        self.frames_grabber.register_frame_callback(self.frame_callback)

        # Init metry grabber
        self.metry_grabber = MetryGrabber(logger, "Metry Angles  ", "Metry Position")
        self.metry_grabber.register_metry_callback(self.metry_callback)

    def grab_loop(self):
        self.metry_grabber.add_listeners()
        self.frames_grabber.run_grab_frames_loop(show = False, save_to_disk = False)

    def stop_grab(self):
        self.metry_grabber.remove_listeners()
    
    @staticmethod
    def frame_callback(frame):
        cv2.imshow("Video", frame)
        # TODO take angles from Q
        #global logger
        #logger.info("New Frame")
    
    @staticmethod
    def metry_callback(angles):
        pass
        # TODO put angles to Q
        #global logger
        #logger.info("New Metry")

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
        grabber.stop_grab()
