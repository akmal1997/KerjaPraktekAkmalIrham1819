from flask import Flask, request, render_template
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import dronekit_sitl
import argparse
vehicle = 0
sitl = 0
class Drone(object):
	global vehicle
	global sitl
	def connect(self):
		sitl = dronekit_sitl.start_default()
		connection_string = sitl.connection_string()
		self.vehicle = connect(connection_string, wait_ready=True)
		
	def takeoff (self, altitude):
		while not self.vehicle.is_armable:
			print "Waiting to initialize..."
			time.sleep(1)
		print "Arming..."
		self.vehicle.mode = VehicleMode("GUIDED")
		self.vehicle.armed = True
		while not self.vehicle.armed:
			print "Waiting for arming..."
			time.sleep(1)
		self.vehicle.simple_takeoff(altitude)
	
	def goto (self, coord):
		self.vehicle.simple_goto(coord)
		
	def disconnect(self):
		#Close vehicle object before exiting script
		print("\nClose vehicle object")
		self.vehicle.close()

	# Shut down simulator if it was started.
		if sitl is not None:
			sitl.stop()

app = Flask(__name__)

d = Drone()

@app.route('/')
def index():
	return render_template("index.html", latitude=str(d.vehicle.location.global_relative_frame.lat), longitude=str(d.vehicle.location.global_relative_frame.lon), altitude=str(d.vehicle.location.global_relative_frame.alt))

@app.route('/connect')
def konek():
	d.connect()
	return "OK, Connected"
	
@app.route('/disconnect')
def diskonek():
	d.disconnect()
	return "OK, disconnected"

@app.route('/track')
def track():
    return str(d.vehicle.location.global_relative_frame)
	
@app.route('/takeoff')
def take_off():
	alt = 2
	d.takeoff(alt)
	while True:
		return str(d.vehicle.location.global_relative_frame.alt)
		if d.vehicle.location.global_relative_frame.alt >= alt*0.95:
			return "Reached target altitude"
			break

@app.route('/goto')
def go_to():
	lat=float(-35.3692605)
	lon=float(149.1612287)
	alt=float(20)
	point = LocationGlobalRelative(lat, lon, alt)
	d.goto(point)
	return str(point)
	
if __name__ == "__main__":
	app.run(host='127.0.0.1', port=5000, threaded=True)