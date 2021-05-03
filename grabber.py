import logging
from grabber_frames import FramesGrabber
from grabber_metry import MetryGrabber
import cv2
import collections

class Grabber():
    def __init__(self, logger):
        self.logger = logger
        
        # Init frames grabber
        self.logger.info("Initiate video grabber")
        self.frames_grabber = FramesGrabber(logger, "Video         ")
        self.frames_grabber.register_frame_callback(self.frame_callback)

        # Init metry grabber
        self.logger.info("Initiate metry grabber")
        self.metry_grabber = MetryGrabber(logger, "Metry Angles  ", "Metry Position")
        self.metry_grabber.register_metry_callback(self.metry_callback)

    def grab_loop(self):
        self.logger.info("Add metry listeners and start grab frames loop")
        self.metry_grabber.add_listeners()
        self.frames_grabber.run_grab_frames_loop(show = False, save_to_disk = False)

    def stop_grab(self):
        self.logger.info("Stop grabbing")
        self.metry_grabber.remove_listeners()
    
    @staticmethod
    def frame_callback(frame):
        global logger
        
        # Take angles from Q
        global metry_queue
        try:
            angles = metry_queue[0]
            logger.info("Frame metry yaw {:.4f} pitch {:.4f} roll {:.4f}".format(angles["yaw"], angles["pitch"], angles["roll"]))
        except IndexError:
            angles = {"NoMetry": True}
            logger.info(angles)
            

        # Show frame
        cv2.imshow("Video", frame)
        
    
    @staticmethod
    def metry_callback(angles):
        #global logger
        #logger.info("New Metry")

        # Put angles to Q
        global metry_queue
        metry_queue.append(angles)


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

    with open("version.txt", "r") as ver_file:
        version = float(ver_file.read())
    
    logger.info("Welcome to Grabber v{}".format(version))
    
    metry_queue = collections.deque(maxlen=1) # TODO move it from this scope. Somehow..
    
    grabber = Grabber(logger)

    try:
        grabber.grab_loop()
    except KeyboardInterrupt:
        logger.info("Ctrl+C pressed")
        grabber.stop_grab()
