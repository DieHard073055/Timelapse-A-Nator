import RPi.GPIO as GPIO
import time

#variables
leds =[16, 20, 21]
switches = [27, 22, 4, 17]

STATE = True
BOOT_READY = True
TIMELAPSE_READY = False
TIMELAPSE_STATE = False

GPIO.setmode(GPIO.BCM)


def led(num, state):
    GPIO.output(num, state)

def blink(l, delay):
    led(l, True)
    time.sleep(delay)
    led(l, False)
    time.sleep(delay)

def setup():
    print "---GPIO Setup---"

    #Turn off warnings from the GPIO library
    GPIO.setwarnings(False)

    #initialise all outputs
    for i in leds:
        GPIO.setup(i, GPIO.OUT)

    print "---GPIO Setup Complete---"

def setup_interrupt(input, cb):
    GPIO.setup(input, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(input, GPIO.FALLING, callback=cb, bouncetime=300)


def remove_interrupt(input):
    GPIO.remove_event_detect(input)

def wait_port(input):
    GPIO.wait_for_edge(input, GPIO.FALLING)

def done_boot_animation():
    for i in leds:
        led(i, True)
    time.sleep(0.05)
    for i in leds:
        led(i, False)
        time.sleep(0.05)

def timelapse_ready_animation():
    led(leds[1], True)
    time.sleep(0.05)
    led(leds[1], False)
    time.sleep(0.05)

def end():
    for i in leds:
        led(i, False)

    GPIO.cleanup()
    print "GPIO pins has been released"



#State variable manipulators

def state_activate():
    global STATE
    STATE = True
    print "---Boot Script Up and Running---"

def state_deactivate():
    global STATE
    STATE = False
    print "---Boot Script Shutting Down---"

def boot_activate():
    global BOOT_READY
    BOOT_READY = True
    print "---No Activity Running---"

def boot_deactivate():
    global BOOT_READY
    BOOT_READY = False

def timelapse_ready_activate():
    global TIMELAPSE_READY
    TIMELAPSE_READY = True
    print "---Timelapse is done setting up---"

def timelapse_ready_deactivate():
    global TIMELAPSE_READY
    TIMELAPSE_READY = False

def timelapse_state_activate():
    global TIMELAPSE_STATE
    TIMELAPSE_STATE = True
    print "---Timelapse has Started---"

def timelapse_state_deactivate():
    global TIMELAPSE_STATE
    TIMELAPSE_STATE = False
    print "---Timelapse has Stopped---"
