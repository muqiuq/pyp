import ssd1306
import machine
import gfx
import pyb


class HelloFilm():
	"""docstring for HelloFilm"""
	def __init__(self):
		self.i2c = pyb.I2C(2)
		self.i2c.init(pyb.I2C.MASTER, baudrate=400000)

		self.oled = ssd1306.SSD1306_I2C(128, 64, self.i2c)

		self.graphics = gfx.GFX(128, 64, self.oled.pixel)

		self.oled.fill(0)

		self.film = [self.__face, self.__hello1, self.__face, 
					self.__hello2,self.__hello3,self.__hello4,self.__hello5,
					self.__hello6,
					self.__face]
		
	def __clear(self):
		self.oled.fill(0)

	def __show(self):
		self.oled.show()

	def display_face(self):
		self.__clear()
		self.__face()
		self.__show()

	def __face(self):
		self.graphics.fill_circle(64-20, 15, 15, 1)
		self.graphics.fill_circle(64+20, 15, 15, 1)

		y = 45
		d = 1
		for x in range(64-15, 64+15):
			self.oled.pixel(x,y,1)
			if x % 3 == 0:
				if y >= 50:
					d = -d
				y += d

	def __hello1(self):
	    self.oled.text('Hi', 50, 20)
	    self.oled.text('Tobi', 40, 30)

	def __hello2(self):
		self.oled.text('My name is', 20, 20)
		self.oled.text('Pyp', 20, 30)

	def __hello3(self):
		self.oled.text('Phipsi told me', 0, 0)
		self.oled.text('that I\'m going',0,10)
		self.oled.text('to stay with you', 0, 20)

	def __hello4(self):
		self.__hello3()
		self.oled.text('Can you take', 0, 30)
		self.oled.text('care of me?', 5, 40)
		

	def __hello5(self):
		self.oled.text('I don\'t wanna', 0, 0)	
		self.oled.text(' be alone... :(',0,10)

	def __hello6(self):
		self.__hello5()
		self.oled.text(' *schnuef*',10,25)

	def play(self):
		for f in self.film:
			self.__clear()
			f()
			self.__show()
			pyb.delay(3000)


