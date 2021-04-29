from __future__ import print_function
from dronekit import connect, VehicleMode
import time
import logging

'''
Callback definition (vehicle observers)
Callback functions should have the following args:
'vehicle'   - the associated vehicle object (used if a callback is different for multiple vehicles)
'attr_name' - the observed attribute (used if callback is used for multiple attributes)
'value'     - the updated attribute value.
'''
def attitude_callback(vehicle, attr_name, value):
    #vehicle.metry_grabber_context.logger.info("{}".format(value))
    vehicle.metry_grabber_context.logger.info("yaw {:.4f} pitch {:.4f} roll {:.4f}".format(value.yaw, value.pitch, value.roll))
    # Only publish when value changes
    #if value!=vehicle.metry_grabber_context.last_attitude_cache:
    #    vehicle.metry_grabber_context.logger.info("{}".format(value))
    #    vehicle.metry_grabber_context.last_attitude_cache=value

def location_callback(vehicle, attr_name, value):
    vehicle.metry_grabber_context.logger.info("{}".format(value))


class MetryGrabberContext():
    def __init__(self, logger):
        self.logger = logger
        self.last_attitude_cache = None

class MetryGrabber():
    def __init__(self, logger):
        self.logger = logger

        # Connect to the Vehicle. 
        pixhawk_device = "/dev/ttyACM0"
        logger.info("Connecting to vehicle on: %s" % pixhawk_device)
        self.vehicle = connect(pixhawk_device, wait_ready=False) #  Set wait_ready=True to ensure default attributes are populated before connect() returns.
        self.vehicle.wait_ready('autopilot_version')
        
        # Add grabber context to the vehicle object
        self.vehicle.metry_grabber_context = MetryGrabberContext(self.logger)

        # Get all vehicle attributes (state)
        self.logger.debug("\nGet all vehicle attribute values:")
        self.logger.debug(" Autopilot Firmware version: %s" % self.vehicle.version)
        self.logger.debug("   Major version number: %s" % self.vehicle.version.major)
        self.logger.debug("   Minor version number: %s" % self.vehicle.version.minor)
        self.logger.debug("   Patch version number: %s" % self.vehicle.version.patch)
        self.logger.debug("   Release type: %s" % self.vehicle.version.release_type())
        self.logger.debug("   Release version: %s" % self.vehicle.version.release_version())
        self.logger.debug("   Stable release?: %s" % self.vehicle.version.is_stable())
        self.logger.debug(" Autopilot capabilities")
        self.logger.debug("   Supports MISSION_FLOAT message type: %s" % self.vehicle.capabilities.mission_float)
        self.logger.debug("   Supports PARAM_FLOAT message type: %s" % self.vehicle.capabilities.param_float)
        self.logger.debug("   Supports MISSION_INT message type: %s" % self.vehicle.capabilities.mission_int)
        self.logger.debug("   Supports COMMAND_INT message type: %s" % self.vehicle.capabilities.command_int)
        self.logger.debug("   Supports PARAM_UNION message type: %s" % self.vehicle.capabilities.param_union)
        self.logger.debug("   Supports ftp for file transfers: %s" % self.vehicle.capabilities.ftp)
        self.logger.debug("   Supports commanding attitude offboard: %s" % self.vehicle.capabilities.set_attitude_target)
        self.logger.debug("   Supports commanding position and velocity targets in local NED frame: %s" % self.vehicle.capabilities.set_attitude_target_local_ned)
        self.logger.debug("   Supports set position + velocity targets in global scaled integers: %s" % self.vehicle.capabilities.set_altitude_target_global_int)
        self.logger.debug("   Supports terrain protocol / data handling: %s" % self.vehicle.capabilities.terrain)
        self.logger.debug("   Supports direct actuator control: %s" % self.vehicle.capabilities.set_actuator_target)
        self.logger.debug("   Supports the flight termination command: %s" % self.vehicle.capabilities.flight_termination)
        self.logger.debug("   Supports mission_float message type: %s" % self.vehicle.capabilities.mission_float)
        self.logger.debug("   Supports onboard compass calibration: %s" % self.vehicle.capabilities.compass_calibration)
        self.logger.debug(" Global Location: %s" % self.vehicle.location.global_frame)
        self.logger.debug(" Global Location (relative altitude): %s" % self.vehicle.location.global_relative_frame)
        self.logger.debug(" Local Location: %s" % self.vehicle.location.local_frame)
        self.logger.debug(" Attitude: %s" % self.vehicle.attitude)
        self.logger.debug(" Velocity: %s" % self.vehicle.velocity)
        self.logger.debug(" GPS: %s" % self.vehicle.gps_0)
        self.logger.debug(" Gimbal status: %s" % self.vehicle.gimbal)
        self.logger.debug(" Battery: %s" % self.vehicle.battery)
        self.logger.debug(" EKF OK?: %s" % self.vehicle.ekf_ok)
        self.logger.debug(" Last Heartbeat: %s" % self.vehicle.last_heartbeat)
        self.logger.debug(" Rangefinder: %s" % self.vehicle.rangefinder)
        self.logger.debug(" Rangefinder distance: %s" % self.vehicle.rangefinder.distance)
        self.logger.debug(" Rangefinder voltage: %s" % self.vehicle.rangefinder.voltage)
        self.logger.debug(" Heading: %s" % self.vehicle.heading)
        self.logger.debug(" Is Armable?: %s" % self.vehicle.is_armable)
        self.logger.debug(" System status: %s" % self.vehicle.system_status.state)
        self.logger.debug(" Groundspeed: %s" % self.vehicle.groundspeed)    # settable
        self.logger.debug(" Airspeed: %s" % self.vehicle.airspeed)    # settable
        self.logger.debug(" Mode: %s" % self.vehicle.mode.name)    # settable
        self.logger.debug(" Armed: %s" % self.vehicle.armed)    # settable
        
        self.logger.info("Init complete")

    def add_listeners(self):
        self.logger.info("Add vehicle attribute")
        
        self.vehicle.add_attribute_listener('attitude', attitude_callback)
        self.vehicle.add_attribute_listener('global_frame', location_callback)

    def remove_listeners(self):
        self.logger.info("Remove vehicle attribute observers")

        self.vehicle.remove_attribute_listener('attitude', attitude_callback)
        self.vehicle.remove_attribute_listener('global_frame', location_callback)


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

    logger.info("Welcome to Metry Grabber")

    metry_grabber = MetryGrabber(logger)
    metry_grabber.add_listeners()
    logger.info("Wait 2s so callback invoked before observer removed")
    time.sleep(2)
    metry_grabber.remove_listeners()

    logger.info("Finished")