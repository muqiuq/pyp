# PYP - PYthon Phipsi Robot

## Introduction
The PYP is a simple robot based on the 2WD Beginner Robot Chassis from robotshop.com and pyboard from micropython.org. 

Originaly this repository was created as a gift for a very good friend of mine.

## Parts
 - [2WD Beginner Robot Chassis](http://www.robotshop.com/ca/en/2wd-beginner-robot-chassis.html)
 - [MicroPython pyboard v1.1 with headers](https://store.micropython.org/store/#/products/PYBv1_1H)
 - SYB-170 breadboard
 - HC-SR04 ultrasonic range detector
 - I2C SSD1306 monochrome oled display 128x64
 - L7805V 5V regulator
 - a lot of jumper wires

## Quickstart
### Important
Switch off the board power suppy from the battery when connecting PYP to the computer (use the switch on the breadboard).

### Startup process
When the pyboard is powered,the kernel first loads boot.py and then by default main.py. For more information about the pyboard look [here](http://docs.micropython.org/en/latest/pyboard/pyboard/general.html?highlight=boot).

### REPL (Console) access (Windows)
 - Download [putty.exe](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html)
 - Connect your pyboard to the computer with a micro usb cable
 - Check the assigned COM port in the device manager
 - Open putty.exe
 - Select Serial and insert the correct port number and set the baud rate to 115200
 - connect
 - Softrestart: Ctrl + D
 - Interupt current application: Ctrl + C

### Edit programs
When you connect your pyboard to the pc a new volume will appear. You can edit and run your program without disconnecting the volume first. 

### Run example program
There is one example program supplied with PYP. You can choose one of two options to run the application:
 - Copy example/example1.py to main.py (dirty)
 - Change the default application script in boot.py to example/example1.py

## Documentation
 - [Micropython](http://docs.micropython.org/en/latest/pyboard/)

For more information visit the repository at https://github.com/muqiuq/pyp
