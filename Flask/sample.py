from flask_wtf import FlaskForm
from wtforms import FloatField, PasswordField, SubmitField, BooleanField, SelectField, TextField, IntegerField
from wtforms.validators import DataRequired, Email, IPAddress, NumberRange
from flask import Flask, request, render_template, redirect, url_for
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import dronekit_sitl
import argparse
import math

username = 0
loggedin = 0
vehicle = 0
sitl = 0
connected = 0
temp = 0
fly = 0
la = 0
lo = 0
remainingDistance = 0
waypoint = []
groundspeed = []
wp = []

class connectform (FlaskForm):
	CONNECTION_TYPE = [('tcp', 'TCP'), ('udp', 'UDP')]
	conn = SelectField('Connection Type', choices=CONNECTION_TYPE)
	ip = TextField('IP Address:', validators=[IPAddress(message='Must be a valid IP Address')])
	port = IntegerField('Port:', validators=[DataRequired()])
	lat = FloatField('Latitude', validators=[DataRequired(), NumberRange(min=-90, max=90, message='Latitude must be -90 to 90')])
	lon = FloatField('Longitude', validators=[DataRequired(), NumberRange(min=-180, max=180, message='Longitude must be -180 to 180')])
	submit = SubmitField('Connect!')

class loginform (FlaskForm):
	username = TextField('Username:', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Log in!')

class WaypointForm(FlaskForm):
    #global username
    lat = FloatField('Latitude', validators=[DataRequired(), NumberRange(min=-90, max=90, message='Latitude must be -90 to 90')])
    lon = FloatField('Longitude', validators=[DataRequired(), NumberRange(min=-180, max=180, message='Longitude must be -180 to 180')])
    alt = FloatField('Altitude', validators=[DataRequired(), NumberRange(min=0, message='Altitude at least 0')])
    gspeed = FloatField('Ground Speed (km/h) (type -1 if you want to null)')
    #remember_me = BooleanField('Remember Me')
    #new_wp = SubmitField('New Waypoint!')
    submit = SubmitField('Add New Waypoint!')

class TakeoffForm(FlaskForm):
    #global username
    alti = FloatField('Altitude', validators=[DataRequired(), NumberRange(min=0, message='Altitude at least 0')])
    #remember_me = BooleanField('Remember Me')
    submit = SubmitField('Takeoff!')

class Drone(object):
	global vehicle
	global sitl
	
	def connect(self, connection_type, ip_address, port, latitude, longitude):
		self.sitl = dronekit_sitl.start_default()
		a = str(latitude)
		b = str(longitude)
		sitl_args = ['-I0', '--model', 'quad']
		sitl_args.append('--home=' + a + ',' + b + ',0,180')
		self.sitl.launch(sitl_args, await_ready=True, restart=True)
		connection_string = connection_type + ":" + ip_address + ":" + port
		print connection_string
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
	
	def goto (self, wp, gs):
		if gs <=0:
			self.vehicle.simple_goto(wp)
			print 'Go to', wp
		else:
			self.vehicle.simple_goto(wp, groundspeed=gs)
			print 'Go to', wp, "Groundspeed" , gs
	
	def land(self):
		self.vehicle.mode = VehicleMode("LAND")
		
	def rtl(self):
		self.vehicle.mode = VehicleMode("LAND")
		
	def disconnect(self):
		#Close vehicle object before exiting script
		print("\nClose vehicle object")
		self.vehicle.close()

	# Shut down simulator if it was started.
		if self.sitl is not None:
			self.sitl.stop()

def get_distance_metres (location1, location2):
	dlat = location2.lat - location1.lat
	dlong = location2.lon - location1.lon
	return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5
	
def clearwayp():
	global temp
	del waypoint[:]
	del groundspeed[:]
	temp=0
	print waypoint,groundspeed,temp

d = Drone()

app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = 'my key'
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
#socketio = SocketIO(app)

@app.route('/carapakai')
def how_to_use():
	return render_template("carapakai.html")
@app.route('/')
def main_menu():
	return render_template("menu.html")
@app.route('/aboutus')
def about_us():
	return render_template("aboutus.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
	global username, loggedin
	if loggedin == 1:
		return redirect('/')
	else:
		forms = loginform()
		if forms.validate_on_submit():
			name = forms.username.data
			password = forms.password.data
			print name, password
			if (name == 'admin' and password == 'admin'):
				loggedin = 1
				username = name
				return render_template('login_sukses.html')
			else:
				return render_template('login_gagal.html')
		return render_template('login.html', form=forms)


@app.route('/connect', methods = ['GET', 'POST'])
def konek_aksi():
	global connected, la, lo, loggedin
	if loggedin == 0:
		return redirect('/login')
	else:
		if connected == 1:
			return redirect('/menu')
		else:
			forms = connectform()
			if forms.validate_on_submit():
				con_type = forms.conn.data
				ip_addr = forms.ip.data
				ports = forms.port.data
				la = forms.lat.data
				lo = forms.lon.data
				print con_type
				print ip_addr
				print ports
				d.connect(con_type, ip_addr, str(ports), la, lo)
				connected=1
				print connected
				print ("Connected! Set home location:" + str(la) + ',' + str(lo))
				return render_template("connect_sukses.html")
			return render_template('connect.html', form=forms)

@app.route('/disconnect')
def diskonek():
	global connected, fly
	clearwayp()
	d.disconnect()
	connected = 0
	fly = 0
	print connected
	return redirect('/connect')

@app.route('/takeoff', methods = ['GET', 'POST'])
def takeoff():
	global fly, connected
	if connected == 0:
		return redirect('/connect')
	else:
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
		fly = 1
		return render_template('takeoff.html', form=form2)

@app.route('/track')
def track():
    return str(d.vehicle.location.global_relative_frame)
	
@app.route('/waypoint', methods = ['GET', 'POST'])
def waypoints():
    form = WaypointForm()
	#if form.
    if form.validate_on_submit():
        lat = form.lat.data
        lon = form.lon.data
        alt = form.alt.data
        gs = form.gspeed.data
        waypoint.append(LocationGlobalRelative(lat, lon, alt))
        groundspeed.append(gs)
		#wp.append()
        for i in range(0,len(waypoint)):
		    print 'Waypoint #', i,':',waypoint[i].lat, waypoint[i].lon, waypoint[i].alt, groundspeed[i]
        #point = LocationGlobalRelative(lat, lon, alt)
        #d.goto(point, gs)
        #return redirect('/menu')
        #return redirect('/index')
    return render_template('waypoint.html', form=form, result=waypoint, res=groundspeed)
	
@app.route('/goto')
def goto():
	global temp, waypoint, fly, remainingDistance
	if fly == 0:
		return render_template("gotoerror.html")
	else:
		if len(waypoint) == 0:
			return redirect('/waypoint')
		else:
			for i in range(temp,len(waypoint)):
				targetDistance = get_distance_metres(d.vehicle.location.global_frame, waypoint[i])
				print 'Go to Waypoint', temp
				if groundspeed[i] == -1:
					d.goto(waypoint[i], -1)
				else:
					d.goto(waypoint[i], (groundspeed[i]/3.6))
				temp = temp + 1;
				while d.vehicle.mode.name == 'GUIDED':
					remainingDistance = get_distance_metres(d.vehicle.location.global_frame, waypoint[i])
					#print "Distance to waypoint", i,":", remainingDistance
					if remainingDistance <= targetDistance * 0.01:
						#print "Reached Target"
						break
					#time.sleep(3)
			return redirect('/menu')
	
@app.route('/menu')
def index():
	global connected, remainingDistance
	if connected == 0:
		return redirect('/connect')
	else:
		return render_template("index.html", latitude=str(d.vehicle.location.global_relative_frame.lat), longitude=str(d.vehicle.location.global_relative_frame.lon), altitude=str(d.vehicle.location.global_relative_frame.alt), battery =str(d.vehicle.battery.level), airspeed=str(d.vehicle.airspeed*3.6), groundspeed=str(d.vehicle.groundspeed*3.6), way = str(temp), head=str(d.vehicle.heading), wp=waypoint, las=la, los=lo, rem= remainingDistance)
	#return render_template('index.html', latitude=7.25, longitude=2.43, altitude=100, groundspeed=45)
@app.route('/clearwp')
def clearwp():
	global fly
	if fly == 1:
		return render_template("clearwperror.html")
	#d.disconnect()
	else:
		clearwayp()
		return redirect('/menu')
	
@app.route('/land')
def landing():
	global fly, la, lo
	d.land()
	fly = 0
	#la = d.vehicle.location.global_relative_frame.lat
	#lo = d.vehicle.location.global_relative_frame.lon
	return render_template("landing_sukses.html")

@app.route('/rtl')
def launch():
	global temp
	d.rtl()
	temp = 0
	return redirect('/menu')

@app.route('/logout')
def logout():
	global loggedin, connected, fly
	if loggedin == 0:
		return redirect('/')
	loggedin = 0
	connected = 0
	fly = 0
	clearwayp()
	d.disconnect()
	return redirect('/')
	
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, threaded=True)
	#socketio.run(app, port=5000)
