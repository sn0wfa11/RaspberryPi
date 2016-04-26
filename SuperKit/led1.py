#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

LedPin = 11 # Pin 11

GPIO.setmode(GPIO.BOARD)
GPIO.SETUP(LedPin, GPIO.OUT)
GPIO.output(LedPin, GPIO.HIGH)

try:
	while True:
		print '...led on'
		GPIO.output(LedPin, GPIO.LOW)
		time.sleep(0.5)
		print '...led off'
		GPIO.output(LedPin, GPIO.HIGH)
		time.sleep(0.5)
except KeybaordInterrupt:
	GPIO.output(LedPin, High)
	GPIO.cleanup()
