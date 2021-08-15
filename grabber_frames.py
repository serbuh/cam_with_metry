from rateCounter import rateCounter
import logging
import cv2
import sys

class FramesGrabber():
    def __init__(self, logger, rateCounterName):
        self.logger = logger
        # Open the camera device
        self.capture_device = cv2.VideoCapture(0) # Use the camera ID based on /dev/videoID

        #Check if camera was opened correctly
        if not (self.capture_device.isOpened()):
            self.logger.error("Could not open video device")
            sys.exit()

        #Set the resolution
        self.capture_device.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture_device.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # init rateCounter
        msg_timeout = 5                         # messages timeout (in seconds). After that priod "No <message name>" will be printed
        print_rate = 2                          # print messages rate every <print_rate> seconds
        self.videoCounter  = rateCounter.rateCounter(rateCounterName,  32, msg_timeout, print_rate, to_print = True, logger = self.logger)

        # Declare callback
        self.callback = None

    def register_frame_callback(self, callback):
        self.callback = callback

    def run_grab_frames_loop(self, show = True, save_to_disk = False):
        # Capture frame-by-frame
        while(True):
            ret, frame = self.capture_device.read()

            self.videoCounter.newMessage()
            self.videoCounter.printRate(print_immediately = False)

            if show:
                # Display the resulting frame
                cv2.imshow("preview",frame)
            
            if save_to_disk: # TODO save to the folder, with indexed name (%ddd...)
                # Save to disk
                cv2.imwrite("outputImage.jpg", frame)

            # Call the callback
            self.callback(frame)

            # Waits for a user input to quit the application NOTE: Even if the opencv window opened from the calling module
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # When everything done, release the resources
        self.quit_capture()
    
    def quit_capture(self):
        self.capture_device.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":

    # Init logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.info("Welcome to Frame Grabber")

    def frame_callback(frame):
        #logger.info("New frame!")
        
        # Display the resulting frame
        cv2.imshow("preview",frame)
        

    frames_grabber = FramesGrabber(logger)
    frames_grabber.register_frame_callback(frame_callback)
    frames_grabber.run_grab_frames_loop(show = False, save_to_disk = False)

    logger.info("Finished")
