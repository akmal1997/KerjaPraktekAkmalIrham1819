from dronekit import connect, VehicleMode, LocationGlobalRelative
from dronekit_sitl import SITL
import time
import math
import dronekit_sitl

sitl = dronekit_sitl.start_default()
connection_string = sitl.connection_string()
vehicle = connect(connection_string, wait_ready=True)

#Close vehicle object before exiting script
print "Close vehicle object"
vehicle.close()

# Shut down simulator if it was started.
if sitl is not None:
    sitl.stop()