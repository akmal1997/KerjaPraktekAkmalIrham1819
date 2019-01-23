from dronekit import connect, VehicleMode, LocationGlobalRelative
from dronekit_sitl import SITL
import time
import math
import dronekit_sitl

sitl = dronekit_sitl.start_default()
connection_string = sitl.connection_string()

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
waypoint.append(LocationGlobalRelative(-6.266667, 106.955555, 20))
waypoint.append(LocationGlobalRelative(-6.2956779, 106.948596, 30))

print len(waypoint)

print "Going towards first point for 30 seconds ..."
targetDistance = get_distance_metres(vehicle.location.global_frame, waypoint[0])
vehicle.simple_goto(waypoint[0])
print vehicle.mode.name

while vehicle.mode.name == "GUIDED":
	remainingDistance = get_distance_metres(vehicle.location.global_frame, waypoint[0])
	print "Distance to target: ", remainingDistance, "Location: ", vehicle.location.global_frame.lat, vehicle.location.global_frame.lon, "Altitude: ", vehicle.location.global_frame.alt
	if remainingDistance <= targetDistance * 0.01:
		print "Reached Target"
		break
	time.sleep(3)

print "Going towards second point for 30 seconds (groundspeed set to 10 m/s) ..."
vehicle.simple_goto(waypoint[1], groundspeed=10)

while vehicle.mode.name == "GUIDED":
	remainingDistance = get_distance_metres(vehicle.location.global_frame, waypoint[1])
	print "Distance to target: ", remainingDistance, "Location: ", vehicle.location.global_frame.lat, vehicle.location.global_frame.lon, "Altitude: ", vehicle.location.global_frame.alt
	if remainingDistance <= targetDistance * 0.01:
		print "Reached Target"
		break
	time.sleep(3)

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