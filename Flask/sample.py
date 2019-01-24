from flask_wtf import FlaskForm
from wtforms import FloatField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email
from flask import Flask, request, render_template, redirect, url_for
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import dronekit_sitl
import argparse

vehicle = 0
sitl = 0
connected = 0
class GoToForm(FlaskForm):
    #global username
    lat = FloatField('Latitude', validators=[DataRequired()])
    lon = FloatField('Longitude', validators=[DataRequired()])
    alt = FloatField('Altitude', validators=[DataRequired()])
    #remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
	
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
	
	def land(self):
		self.vehicle.mode = VehicleMode("LAND")
		
	def disconnect(self):
		#Close vehicle object before exiting script
		print("\nClose vehicle object")
		self.vehicle.close()

	# Shut down simulator if it was started.
		if sitl is not None:
			sitl.stop()

d = Drone()

app = Flask(__name__)
app.secret_key = 'my key'

@app.route('/')
def main_menu():
	return render_template("menu.html")
@app.route('/menu')
def index():
	return render_template("index.html", latitude=str(d.vehicle.location.global_relative_frame.lat), longitude=str(d.vehicle.location.global_relative_frame.lon), altitude=str(d.vehicle.location.global_relative_frame.alt), groundspeed=str(d.vehicle.groundspeed*3.6))

@app.route('/connect')
def konek_aksi():
	d.connect()
	connect=1
	print ("Connected")
	return render_template("connect_sukses.html")
	
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
		#return str(d.vehicle.location.global_relative_frame.alt)
		return render_template("takeoff_sukses.html")
		if d.vehicle.location.global_relative_frame.alt >= alt*0.95:
			return "Reached target altitude"
			break

@app.route('/goto', methods = ['GET', 'POST'])
def goto():
    form = GoToForm()
    if form.validate_on_submit():
        lat = form.lat.data
        lon = form.lon.data
        alt = form.alt.data
        #print (lat)
        #print (lon)
        #print (alt)
        point = LocationGlobalRelative(lat, lon, alt)
        d.goto(point)
        return redirect('/menu')
        #return redirect('/index')
    return render_template('goto.html', title='Sign In', form=form)
	#lat=float(-35.3692605)
	#lon=float(149.1612287)
	#alt=float(20)
	#point = LocationGlobalRelative(lat, lon, alt)
	#d.goto(point)
	#return str(point)

@app.route('/land')
def landing():
	d.land()
	return render_template("landing_sukses.html")
	
if __name__ == "__main__":
	app.run(host='127.0.0.1', port=5000, threaded=True)
