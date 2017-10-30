#!/usr/bin/env python
import RPi.GPIO as gpio
from time import *

led1 = 18

def setup():
	gpio.setmode(gpio.BCM)
	gpio.setup(led1, gpio.OUT)
	gpio.output(led1, gpio.HIGH)

def loop():
	while True:
		led_on(led1)
		sleep(0.5)
		led_off(led1)
		sleep(0.5)

def led_on(pin):
	gpio.output(pin, gpio.LOW)

def led_off(pin):
	gpio.output(pin, gpio.HIGH)

def destroy():
	gpio.cleanup()
		
if __name__ == '__main__':
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()
	destroy()
