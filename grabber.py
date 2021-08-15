import logging
from grabber_frames import FramesGrabber
from grabber_metry import MetryGrabber
import cv2
import collections
import tkinter
import math

class Grabber():
    def __init__(self, logger, metry_queue):
        self.logger = logger
        
        # Print grabber version
        with open("version.txt", "r") as ver_file:
            version = float(ver_file.read())
        self.logger.info("Welcome to Grabber v{}".format(version))

        # Init frames grabber
        self.logger.info("Initiate video grabber")
        self.frames_grabber = FramesGrabber(logger, "Video         ")
        self.frames_grabber.register_frame_callback(self.frame_callback)

        # Init metry grabber
        self.logger.info("Initiate metry grabber")
        self.metry_grabber = MetryGrabber(logger, metry_queue, "Metry Angles  ", "Metry Position")
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
            yaw = math.degrees(angles["yaw"])
            pitch = math.degrees(angles["pitch"])
            roll = math.degrees(angles["roll"])
            
            logger.info("Frame metry yaw {:.2f} pitch {:.2f} roll {:.2f}".format(yaw, pitch, roll))
        except IndexError:
            logger.info("NoMetry")
            

        # Show frame
        cv2.imshow("Video", frame)
        
    
    @staticmethod
    def metry_callback(angles):
        #global logger
        #logger.info("New Metry")

        # Put angles to Q
        global metry_queue
        metry_queue.append(angles)
    
    def other(self, angles):
        self.metry_queue.apend(angles)



if __name__ == "__main__":

    # Init logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Init logger console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    metry_queue = collections.deque(maxlen=1)

    grabber = Grabber(logger, metry_queue)

    try:
        grabber.grab_loop()
    except KeyboardInterrupt:
        logger.info("Ctrl+C pressed")
        grabber.stop_grab()
