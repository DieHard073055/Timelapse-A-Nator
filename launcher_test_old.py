#Imports
import RPi.GPIO as GPIO
import sys
import time
import random

#init leds and switches
data_pin = 13
latch_pin = 19
clock_pin = 26

leds =[16, 20, 21]
switches = [27, 22, 4, 17]

STATE = True


def stopanimation(channel):
	print "channel : " + str(channel)
	print "Releasing the GPIO pins"
	GPIO.cleanup()
	print "Program exiting"
	exit(0)

def start_timelapse(channel):

	GPIO.cleanup()
#	import os
#	os.system("raspistill -t 5000000 -tl 10000 -o /home/pi/pics/image%04d.jpg")

def setup():

	#set GPIO library to use GPIO numbers
	GPIO.setmode(GPIO.BCM)

	#Turn off warnings
	GPIO.setwarnings(False)

	#init all the output modes
	for i in leds:
		GPIO.setup(i, GPIO.OUT)

	GPIO.setup(data_pin, GPIO.OUT)
	GPIO.setup(latch_pin, GPIO.OUT)
	GPIO.setup(clock_pin, GPIO.OUT)

	#Setup switches [2](tac switch pin 4)
	GPIO.setup(switches[2], GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(switches[2], GPIO.FALLING, callback=stopanimation, bouncetime=300)

	#Setup timelapse on switch[3](tac switch on pin 17)
	GPIO.setup(switches[3], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(switches[3], GPIO.FALLING, callback=start_timelapse, bouncetime=300)

	print "GPIO Setup Complete"

def main():
	while(1):
		for x in xrange(5):
			led_run()
		for x in xrange(5):
			led_blink()
		for x in range(5):
			led_random()
		#matrix_basic()

def matrix_basic():
	delay = 0.1
        while(1):
        	delay = matrix_animate_basic(delay)

def matrix_animate_basic(delay):
	anode = [[1, 0, 0, 0,], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        cathode = [[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]]
        for x in xrange(len(anode)):
                for y in xrange(len(cathode)):
                        for i in anode[x]:
                                if i:
                                        data_high()

                                else:
                                        data_low()
                                clock()
                        for i in cathode[y]:
                                if i:
                                        data_high()
                                else:
                                        data_low()
                                clock()
                        latch()
                        time.sleep(delay)
                delay = delay - (0.1 * delay)
                if delay < 0.0009:
                        delay = 0.1

        for x in xrange(len(anode)):
                for y in xrange(len(cathode)):
                        for i in anode[y]:
                                if i:
                                        data_high()
				else:
                                        data_low()
                                clock()
                        for i in cathode[x]:
                                if i:
                                        data_high()
                                else:
                                        data_low()
                                clock()
                        latch()
                        time.sleep(delay)

                delay = delay - (0.1 * delay)
                if delay < 0.0009:
                        delay = 0.1
        return delay


def led_run():

	for i in range(len(leds)):
		led(leds[i], True)
		time.sleep(0.05)
		led(leds[i], False)

	for i in range(len(leds)):
		led(leds[(len(leds)-1)-i], True)
		time.sleep(0.05)
		led(leds[(len(leds)-1)-i], False)

def led_blink():

	for i in leds:
		led(i, True)
	time.sleep(0.05)
	for i in leds:
		led(i, False)
	time.sleep(0.05)

def led_random():
	i = random.randint(0, 2)
	for x in range(512, 0):
		pwm(leds[i], x)
	for x in range(0, 512):
		pwm(leds[i], x)

def pwm(l, val):
	for x in xrange(512):
		if x > val:
			led(l, True)
		else:
			led(l, False)
	#	time.sleep(0.000002)

def led(num, state):
	GPIO.output(num, state)

def data_high():
        GPIO.output(data_pin, True)

def data_low():
        GPIO.output(data_pin, False)

def clock():
        GPIO.output(clock_pin, True)
        GPIO.output(clock_pin, False)

def latch():
        GPIO.output(latch_pin, False)
        GPIO.output(latch_pin, True)

if __name__ == '__main__':
	print sys.argv
	setup()
	main()
