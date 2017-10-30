#!/usr/bin/python
import RPi.GPIO as GPIO
import time

LedPin = 11

def setup():
  GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
  GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
  GPIO.output(LedPin, GPIO.HIGH) # Set LedPin high(+3.3V) to off led

def push():
  GPIO.output(LedPin, GPIO.LOW)

def release():
  GPIO.output(LedPin, GPIO.HIGH)

def reboot():
  print "Rebooting..."
  print "Shutting Down"
  push()
  time.sleep(10)
  release()
  print "Waiting"
  time.sleep(15)
  print "Powering back on"
  push()
  time.sleep(0.7)
  release()

def destroy():
  release()
  GPIO.cleanup()

def main():
  setup()
  reboot()
  destroy()

if __name__ == '__main__':
  main()

