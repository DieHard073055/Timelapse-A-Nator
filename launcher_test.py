#Boot script for the pi
#---- Load "nothing to do" animation on the leds
#---- When the button on pin 4 is pressed is will load the timelapse script
#---- repeat
from camera import camera as cam
from gpio import gpio as g


def setup():
    g.setup()
    g.setup_interrupt(g.switches[2], stopanimation)

def main():
    print "main"
    while(g.STATE):
        g.done_boot_animation()

    g.end()

def stopanimation(channel):
    g.STATE = False

if __name__ == '__main__':
    setup()
    main()
