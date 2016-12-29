from pyb import Pin, Timer

class Motors:

	SLOWEST = 100
	SLOWER = 1000
	SLOW = 10000
	FAST = 100000
	FASTER = 1000000

	PULSE_WIDTH = 50

	def __init__(self, m_standby = "Y2", m_a_1 = "Y5", m_a_2 = "Y4", m_a_pwm = "Y1", m_a_timer_num = 8, m_a_channel = 1, 
		m_b_1 = "Y7", m_b_2 = "Y6", m_b_pwm = "Y3", m_b_timer_num = 4, m_b_channel = 3):
		self.m_a_1 = m_a_1
		self.m_a_2 = m_a_2
		self.m_a_pwm = m_a_pwm
		self.m_b_1 = m_b_1
		self.m_b_2 = m_b_2
		self.m_b_pwm = m_b_pwm


		self.m_standby = m_standby
		self.pin_standby = Pin(self.m_standby, Pin.OUT)

		self.pin_m_a_1 = Pin(self.m_a_1, Pin.OUT)
		self.pin_m_a_2 = Pin(self.m_a_2, Pin.OUT)
		self.pin_m_a_pwm = Pin(self.m_a_pwm)

		self.m_a_timer_num = m_a_timer_num
		self.m_a_channel = m_a_channel
		
		self.m_b_timer_num = m_b_timer_num
		self.m_b_channel = m_b_channel

		self._speed = Motors.SLOW

		self.timer_a = Timer(self.m_a_timer_num,freq=self._speed)
		self.channel_a = self.timer_a.channel(self.m_a_channel, Timer.PWM, pin=self.pin_m_a_pwm)
		self.channel_a.pulse_width_percent(Motors.PULSE_WIDTH)

		self.pin_m_b_1 = Pin(self.m_b_1, Pin.OUT)
		self.pin_m_b_2 = Pin(self.m_b_2, Pin.OUT)
		self.pin_m_b_pwm = Pin(self.m_b_pwm)

		self.timer_b = Timer(self.m_b_timer_num,freq=self._speed)
		self.channel_b = self.timer_b.channel(self.m_b_channel, Timer.PWM, pin=self.pin_m_b_pwm)
		self.channel_b.pulse_width_percent(Motors.PULSE_WIDTH)

		self.__set_standby(1)

	def __set_standby(self,val):
		self.pin_standby.value(val)

	def __set_m_a(self, val1, val2=None):
		_val1 = val1
		_val2 = val1
		if val2 is not None:
			_val2 = val2
		self.pin_m_a_1.value(_val1)
		self.pin_m_a_2.value(_val2)		

	def __set_m_b(self, val1, val2=None):
		_val1 = val1
		_val2 = val1
		if val2 is not None:
			_val2 = val2
		self.pin_m_b_1.value(_val1)
		self.pin_m_b_2.value(_val2)		

	def stop(self):
		self.__set_m_a(0)
		self.__set_m_b(0)

	def forward(self):
		self.__set_m_a(1,0)
		self.__set_m_b(1,0)

	def speed(self, newspeed):
		self._speed = newspeed
		self.speed_left(newspeed)
		self.speed_right(newspeed)
		
	def speed_left(self, newspeed):
		self.timer_a.freq(newspeed)

	def speed_right(self, newspeed):
		self.timer_b.freq(newspeed)

	def reverse(self):
		self.__set_m_a(0,1)
		self.__set_m_b(0,1)

	def rotate_left(self):
		self.__set_m_a(0,1)
		self.__set_m_b(1,0)

	def rotate_right(self):
		self.__set_m_a(1,0)
		self.__set_m_b(0,1)

	def left_turn(self, factor = 10):
		self.__set_m_a(1,0)
		self.__set_m_b(1,0)
		self.speed_left(self._speed/10)
		self.speed_right(self._speed)

	def right_turn(self, factor = 10):
		self.__set_m_a(1,0)
		self.__set_m_b(1,0)
		self.speed_left(self._speed)
		self.speed_right(self._speed/10)

