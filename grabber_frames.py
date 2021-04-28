from rateCounter import rateCounter
import logging
import cv2

class CameraPlayer():
    def __init__(self, logger):
        self.logger = logger
        # Open the camera device
        self.capture_device = cv2.VideoCapture(0) # Use the camera ID based on /dev/videoID

        #Check if camera was opened correctly
        if not (self.capture_device.isOpened()):
            self.logger.error("Could not open video device")

        #Set the resolution
        self.capture_device.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture_device.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # init rateCounter
        msg_timeout = 5                         # messages timeout (in seconds). After that priod "No <message name>" will be printed
        print_rate = 2                          # print messages rate every <print_rate> seconds
        self.videoCounter  = rateCounter.rateCounter("Video",  20, msg_timeout, print_rate)

    def capture_loop(self):
        # Capture frame-by-frame
        while(True):
            ret, frame = self.capture_device.read()

            self.videoCounter.newMessage()
            self.videoCounter.printRate(print_immediately = False)

            # Display the resulting frame
            cv2.imshow("preview",frame)
            
            # Save to disk
            # cv2.imwrite("outputImage.jpg", frame)

            # Send the frame 
            # TODO get the last telemetry and send together with the frame

            #Waits for a user input to quit the application
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
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.info("Welcome to Frame Grabber")

    cam_player = CameraPlayer(logger)
    cam_player.capture_loop()