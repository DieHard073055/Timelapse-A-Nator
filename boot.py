#Boot script for the pi
#---- Load "nothing to do" animation on the leds
#---- When the button on pin 4 is pressed is will load the timelapse script
#---- repeat
from camera import camera as cam
from gpio import gpio as g
import time

direc = ''
pic_num = 0

def setup():
    g.setup()
    g.setup_interrupt(g.switches[2], start_timelapse)
    g.setup_interrupt(g.switches[3], stop)

def animations():
    print "---Led Animations Activated---"
    while(g.STATE):
        if g.BOOT_READY:
            g.done_boot_animation()
        if g.TIMELAPSE_READY:
            g.timelapse_ready_animation()
    print "---Led Animations Deactivated---"
    g.end()



def start_timelapse(channel):
    global direc
    global pic_num
    direc = time.strftime("%b-%d-%Y-%H:%M:%S")
    print "---Directory name : " + direc + "---"
    direc = "/home/pi/pics/" + direc + "/"
    cam.setup()
    cam.make_dir(direc)
    pic_num = 0

    setup_timelapse()
    timelapse_main()

def setup_timelapse():
    g.boot_deactivate()
    g.timelapse_ready_activate()

    g.remove_interrupt(g.switches[2])
    print "---Waiting for Input--- "
    g.wait_port(g.switches[2])
    g.remove_interrupt(g.switches[2])
    g.timelapse_ready_deactivate()

def timelapse_main():
    global pic_num
    global direc

    g.timelapse_state_activate()


    while g.TIMELAPSE_STATE == True:
        g.setup_interrupt(g.switches[2], timelapse_stop)
        filename = "image%04d.jpg" % pic_num
        pic_num = pic_num+1
        cam.snap(filename, direc)
        g.blink(g.leds[1], 0.05)
        time.sleep(2)
        g.remove_interrupt(g.switches[2])

    time.sleep(1)
    g.remove_interrupt(g.switches[2])
    g.setup_interrupt(g.switches[2], start_timelapse)
    g.boot_activate()

def timelapse_stop(channel):
    g.timelapse_state_deactivate()

def stop(channel):
    g.STATE = False



if __name__ == '__main__':
    setup()
    animations()
