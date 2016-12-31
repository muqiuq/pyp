# main.py 
# Example for simple obstacle detection
# Wrote by Philipp Albrecht, Zürich, CH
# For more information visit http://pyp.uisa.ch 

# Imports

from pyb import Pin, Timer
from motors import Motors
import time
import ultrasonic
import ssd1306
import machine
import gfx
import ultrasonic

# Init I2C for OLED control

i2c = pyb.I2C(2)
i2c.init(pyb.I2C.MASTER, baudrate=400000)

oled = ssd1306.SSD1306_I2C(128, 64, i2c)

graphics = gfx.GFX(128, 64, oled.pixel)

oled.fill(0)

# Init motors

motors = Motors()

# Init ultrasonic range detector

ultra_echo = Pin('X10')
ultra_trig = Pin('X9')

# Init left & right contact detector

left_contact = Pin('X12', Pin.IN, Pin.PULL_DOWN)
right_contact = Pin('X11', Pin.IN, Pin.PULL_DOWN)


distance_sensor = ultrasonic.Ultrasonic(ultra_trig, ultra_echo)

# Statemachine init

stateChanged = True

class RState():
	WAIT = 0
	LEFT_TURN = 1
	RIGHT_TURN = 2
	FORWARD = 3
	FORWARD_SLOW = 4
	SET_BACK_LEFT = 5
	SET_BACK_RIGHT = 6

class CGlobal():
	DO_GET_DISTANCE = False

currentState = RState.WAIT

def setState(state):
	global currentState
	global stateChanged
	global curr_distance

	if state != currentState:
		stateChanged = True
		currentState = state

	display_distance_and_state(curr_distance, currentState)

doGetDistance = False

def getDistance(t):
	global doGetDistance
	doGetDistance = True

tim = Timer(2, freq=1000)
tim.counter() # get counter value
tim.freq(2) # 0.5 Hz
tim.callback(lambda t: pyb.LED(1).toggle())

tim = pyb.Timer(1)
tim.init(freq=4)
tim.callback(getDistance)

timer_start = time.ticks_ms()

last_distance = 0
curr_distance = 0

# OLED Display function

def display_distance_and_state(distance, state):
	global oled
	oled.fill(0)
	oled.text('cm:', 0, 10)
	oled.text("{:.2f}".format(distance), 80, 10)

	oled.text('State:', 0, 30)
	oled.text("{:d}".format(state), 80, 30)

	oled.show()

# main loop


while True:
	pyb.delay(1)

	# action in case the state changed

	if stateChanged is True:
		print("New State: ", currentState)
		if currentState == RState.LEFT_TURN:
			motors.speed(Motors.SLOWER)
			motors.rotate_left()
			timer_start = time.ticks_ms()

		elif currentState == RState.RIGHT_TURN:
			motors.speed(Motors.SLOWER)
			motors.rotate_right()
			timer_start = time.ticks_ms()

		elif currentState == RState.FORWARD:
			motors.speed(Motors.SLOW)
			motors.forward()

		elif currentState == RState.FORWARD_SLOW:
			motors.speed(Motors.SLOWER)
			motors.forward()

		elif currentState == RState.SET_BACK_LEFT or currentState == RState.SET_BACK_RIGHT:
			motors.speed(Motors.SLOWER)
			motors.reverse()
			timer_start = time.ticks_ms()
		
	stateChanged = False

	# If the timer 1 triggers distance detection (4Hz)

	if doGetDistance == True:
		distance1 = distance_sensor.distance_in_cm()

		if abs(distance1 - last_distance) < 10:
			curr_distance = distance1

		last_distance = distance1

		doGetDistance = False	
		print("Distance: ", curr_distance)
		display_distance_and_state(curr_distance, currentState)

	# State change coditions
	
	time_diff = time.ticks_ms() - timer_start

	if curr_distance is None:
		motors.stop()

		#left_contact

	if currentState == RState.LEFT_TURN and time_diff > 500:
		setState(RState.FORWARD)
	elif currentState == RState.RIGHT_TURN and time_diff > 500:
		setState(RState.FORWARD)
	elif currentState == RState.FORWARD or currentState == RState.FORWARD_SLOW:
		if left_contact.value() != 0:
			setState(RState.SET_BACK_RIGHT)
		elif right_contact.value() != 0:
			setState(RState.SET_BACK_LEFT)
		elif currentState == RState.FORWARD_SLOW:
			if curr_distance < 20:
				setState(RState.SET_BACK_LEFT)
			elif curr_distance > 50:
				setState(RState.FORWARD)

		elif currentState == RState.FORWARD:
			if curr_distance < 40:
				setState(RState.FORWARD_SLOW)

	elif currentState == RState.SET_BACK_LEFT and time_diff > 500:
		setState(RState.LEFT_TURN)
	elif currentState == RState.SET_BACK_RIGHT and time_diff > 500:
		setState(RState.RIGHT_TURN)		
	elif currentState == RState.WAIT and time_diff > 3000:
		setState(RState.FORWARD_SLOW)




