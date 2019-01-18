from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import math


#Set up option parsing to get connection string
import argparse  
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect', 
                   help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None


#Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()


# Connect to the Vehicle
print 'Connecting to vehicle on: %s' % connection_string
vehicle = connect(connection_string, wait_ready=True)


def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print "Basic pre-arm checks"
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print " Waiting for vehicle to initialise..."
        time.sleep(1)

        
    print "Arming motors"
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True    

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:      
        print " Waiting for arming..."
        time.sleep(1)

    print "Taking off!"
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print " Altitude: ", vehicle.location.global_relative_frame.alt 
        #Break and return from function just below target altitude.        
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: 
            print "Reached target altitude"
            break
        time.sleep(1)
def get_distance_metres (location1, location2):
	dlat = location2.lat - location1.lat
	dlong = location2.lon - location1.lon
	return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

arm_and_takeoff(1.80)

print "Set default/target airspeed to 3"
vehicle.airspeed = 9

waypoint = []
print "Going towards first point for 30 seconds ..."
waypoint.append(LocationGlobalRelative(-6.266667, 106.955555, 20))
targetDistance = get_distance_metres(vehicle.location.global_frame, waypoint[0])
vehicle.simple_goto(waypoint[0])

while vehicle.mode.name == "GUIDED":
	remainingDistance = get_distance_metres(vehicle.location.global_frame, waypoint[0])
	print "Distance to target: ", remainingDistance, "Location: ", vehicle.location.global_frame
	if remainingDistance <= targetDistance * 0.01:
		print "Reached Target"
		break
	time.sleep(3)


#print "Going towards second point for 30 seconds (groundspeed set to 10 m/s) ..."
#waypoint.append(LocationGlobalRelative(-6.2656779, 106.948596, 20))
#vehicle.simple_goto(waypoint[1], groundspeed=10)

#time.sleep(30)

#print "Going towards third point for 30 seconds (groundspeed set to 10 m/s) ..."
#waypoint.append(LocationGlobalRelative(-6.2636779, 106.928596, 20))
#vehicle.simple_goto(waypoint[2], groundspeed=10)

# sleep so we can see the change in map
#time.sleep(30)


print("Now let's land")
vehicle.mode = VehicleMode("LAND")
while True:
	print "Altitude: ", vehicle.location.global_relative_frame.alt
	if vehicle.location.global_relative_frame.alt <= 0.05:
		print "Landed"
		break
	time.sleep(1)

#Close vehicle object before exiting script
print "Close vehicle object"
vehicle.close()

# Shut down simulator if it was started.
if sitl is not None:
    sitl.stop()