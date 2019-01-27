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
waypoint = []
groundspeed = []

class connectform (FlaskForm):
	lat = FloatField('Latitude', validators=[DataRequired()])
	lon = FloatField('Longitude', validators=[DataRequired()])
	submit = SubmitField('Connect!')

class GoToForm(FlaskForm):
    #global username
    lat = FloatField('Latitude', validators=[DataRequired()])
    lon = FloatField('Longitude', validators=[DataRequired()])
    alt = FloatField('Altitude', validators=[DataRequired()])
    gspeed = FloatField('Ground Speed (type -1 if you want to null)')
    #remember_me = BooleanField('Remember Me')
    #new_wp = SubmitField('New Waypoint!')
    submit = SubmitField('Go To!')

class TakeoffForm(FlaskForm):
    #global username
    alti = FloatField('Altitude', validators=[DataRequired()])
    #remember_me = BooleanField('Remember Me')
    submit = SubmitField('Takeoff!')

class Drone(object):
	global vehicle
	global sitl
	def connect(self, latitude, longitude):
		self.sitl = dronekit_sitl.start_default()
		a = str(latitude)
		b = str(longitude)
		sitl_args = ['-I0', '--model', 'quad']
		sitl_args.append('--home=' + a + ',' + b + ',0,180')
		self.sitl.launch(sitl_args, await_ready=True, restart=True)
		connection_string = self.sitl.connection_string()
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
	
	def goto (self, coord, speed):
		if speed == -1:
			self.vehicle.simple_goto(coord)
		else:
			self.vehicle.simple_goto(coord, groundspeed=speed)
	
	def land(self):
		self.vehicle.mode = VehicleMode("LAND")
		
	def disconnect(self):
		#Close vehicle object before exiting script
		print("\nClose vehicle object")
		self.vehicle.close()

	# Shut down simulator if it was started.
		if self.sitl is not None:
			self.sitl.stop()

d = Drone()

app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = 'my key'

@app.route('/')
def main_menu():
	return render_template("menu.html")
@app.route('/menu')
def index():
	return render_template("index.html", latitude=str(d.vehicle.location.global_relative_frame.lat), longitude=str(d.vehicle.location.global_relative_frame.lon), altitude=str(d.vehicle.location.global_relative_frame.alt), groundspeed=str(d.vehicle.groundspeed*3.6))
	#return render_template('index.html', latitude=7.25, longitude=2.43, altitude=100, groundspeed=45)
#@app.route('/hehe')
#def static_file():
#	return app.send_static_file('index.html')
@app.route('/connect', methods = ['GET', 'POST'])
def konek_aksi():
	forms = connectform()
	if forms.validate_on_submit():
		la = forms.lat.data
		lo = forms.lon.data
		d.connect(la, lo)
		connect=1
		print ("Connected! Set home location:" + str(la) + ',' + str(lo))
		return render_template("connect_sukses.html")
	return render_template('connect.html', form=forms)

@app.route('/disconnect')
def diskonek():
	d.disconnect()
	return redirect('/')

@app.route('/takeoff', methods = ['GET', 'POST'])
def takeoff():
	form2=TakeoffForm()
	if form2.validate_on_submit():
		altitude = form2.alti.data
		d.takeoff(altitude)
		while True:
			#return str(d.vehicle.location.global_relative_frame.alt)
			return render_template("takeoff_sukses.html")
			if d.vehicle.location.global_relative_frame.alt >= alt*0.95:
				return "Reached target altitude"
				break
		#print altitude
	return render_template('takeoff.html', form=form2)

@app.route('/track')
def track():
    return str(d.vehicle.location.global_relative_frame)
	
#@app.route('/goto_addwp')
#def add_waypoint():
	
@app.route('/goto', methods = ['GET', 'POST'])
def goto():
    form = GoToForm()
	#if form.
    if form.validate_on_submit():
        lat = form.lat.data
        lon = form.lon.data
        alt = form.alt.data
        gs = form.gspeed.data
        print (lat)
        print (lon)
        print (alt)
        print (gs)
        point = LocationGlobalRelative(lat, lon, alt)
        d.goto(point, gs)
        return redirect('/menu')
        #return redirect('/index')
    return render_template('goto.html', form=form)

@app.route('/land')
def landing():
	d.land()
	return render_template("landing_sukses.html")
	
if __name__ == "__main__":
	app.run(host='127.0.0.1', port=5000, threaded=True)
