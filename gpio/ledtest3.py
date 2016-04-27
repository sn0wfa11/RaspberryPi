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
	gpio.setup(button1, gpio.IN, pull_up_down=gpio.PUD_UP)

def switch(pwm_led):
	global led1_status
	if led1_status == False:
		led_up(pwm_led)
		led1_status = True
	else:
		led_down(pwm_led)
		led1_status = False

def loop():
	global button1_status
	pwm_led1 = gpio.PWM(led1, 500)
	pwm_led1.start(100)
	while True:
		if gpio.input(button1) == False:
			if button1_status == False:
				button1_status = True
				switch(pwm_led1)
				sleep(0.2)
		else:
			button1_status = False

def led_on(pin):
	gpio.output(pin, gpio.LOW)

def led_off(pin):
	gpio.output(pin, gpio.HIGH)

def led_up(pwm_led):
	for x in range(0, 101):
		pwm_led.ChangeDutyCycle(x)
		print(x)
		sleep(0.05)

def led_down(pwm_led):
	for x in range (0, 101):
		y = 100 - x
		pwm_led.ChangeDutyCycle(y)
		print(y)
		sleep(0.05)

def destroy():
	gpio.cleanup()
		
if __name__ == '__main__':
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()
