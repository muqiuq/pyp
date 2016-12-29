# main.py -- put your code here!

from pyb import Pin, Timer
from motors import Motors
import time
import ultrasonic
import ssd1306
import machine
import gfx
import ultrasonic


import micropython
micropython.alloc_emergency_exception_buf(100)

i2c = pyb.I2C(2)
i2c.init(pyb.I2C.MASTER, baudrate=400000)

oled = ssd1306.SSD1306_I2C(128, 64, i2c)

graphics = gfx.GFX(128, 64, oled.pixel)

oled.fill(0)

motors = Motors()

ultra_echo = Pin('X10')
ultra_trig = Pin('X9')

distance_sensor = ultrasonic.Ultrasonic(ultra_trig, ultra_echo)

stateChanged = True

class RState():
	WAIT = 0
	LEFT_TURN = 1
	FORWARD = 2
	FORWARD_SLOW = 3
	SET_BACK = 4

class CGlobal():
	DO_GET_DISTANCE = False

currentState = RState.WAIT

def setState(state):
	global currentState
	global stateChanged
	if state != currentState:
		stateChanged = True
		currentState = state

doGetDistance = False

def getDistance(t):
	global doGetDistance
	doGetDistance = True

tim = pyb.Timer(1)
tim.init(freq=4)
tim.callback(getDistance)

timer_start = time.ticks_ms()

last_distance = 0
curr_distance = 0

def display_distance_and_state(distance, state):
	global oled
	oled.fill(0)
	oled.text('cm:', 0, 10)
	oled.text("{:.2f}".format(distance), 80, 10)

	oled.text('State:', 0, 30)
	oled.text("{:d}".format(state), 80, 30)

	oled.show()

while True:
	pyb.delay(1)

	if stateChanged is True:
		print("New State: ", currentState)
		if currentState == RState.LEFT_TURN:
			motors.speed(Motors.SLOWER)
			motors.rotate_left()
			timer_start = time.ticks_ms()

		elif currentState == RState.FORWARD:
			motors.speed(Motors.SLOW)
			motors.forward()

		elif currentState == RState.FORWARD_SLOW:
			motors.speed(Motors.SLOWER)
			motors.forward()

		elif currentState == RState.SET_BACK:
			motors.speed(Motors.SLOWER)
			motors.reverse()
			timer_start = time.ticks_ms()
		
	stateChanged = False

	if doGetDistance == True:
		distance1 = distance_sensor.distance_in_cm()

		if abs(distance1 - last_distance) < 10:
			curr_distance = distance1

		last_distance = distance1

		doGetDistance = False	
		print("Distance: ", curr_distance)
		display_distance_and_state(curr_distance, currentState)

	
	time_diff = time.ticks_ms() - timer_start

	if curr_distance is None:
		motors.stop()

	if currentState == RState.LEFT_TURN and time_diff > 500:
		setState(RState.FORWARD)
	elif currentState == RState.FORWARD_SLOW:
		if curr_distance < 20:
			setState(RState.SET_BACK)
		elif curr_distance > 50:
			setState(RState.FORWARD)

	elif currentState == RState.FORWARD:
		if curr_distance < 40:
			setState(RState.FORWARD_SLOW)

	elif currentState == RState.SET_BACK and time_diff > 500:
		setState(RState.LEFT_TURN)
	elif currentState == RState.WAIT and time_diff > 3000:
		setState(RState.FORWARD_SLOW)




