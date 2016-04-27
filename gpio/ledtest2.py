#!/usr/bin/env python
import RPi.GPIO as gpio
from time import *

led1 = 18
button1 = 12
led1_status = False
button1_status = False

def setup():
	gpio.setmode(gpio.BCM)
	gpio.setup(led1, gpio.OUT)
	gpio.output(led1, gpio.HIGH)
	gpio.setup(button1, gpio.IN, pull_up_down=gpio.PUD_UP)

def switch():
	global led1_status
	if led1_status == False:
		led_on(led1)
		led1_status = True
	else:
		led_off(led1)
		led1_status = False

def loop():
	global button1_status
	while True:
		if gpio.input(button1) == False:
			if button1_status == False:
				button1_status = True
				switch()
				sleep(0.2)
		else:
			button1_status = False

def led_on(pin):
	gpio.output(pin, gpio.LOW)

def led_off(pin):
	gpio.output(pin, gpio.HIGH)

def destroy():
	led_off(led1)
	gpio.cleanup()
		
if __name__ == '__main__':
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()
