import pygame
import pygame.camera
import os

cams = []

def setup():
    global cams
    cams = []
    if not check_for_webcams():
        print "---Camera : Web Cam Detected ---"
        cams = pygame.camera.list_cameras()
    else:
        print "---Camera : No Web Cam Detected"
    print "---Camera : Setup Complete---"

def make_dir(direc):
    global cams
    cmd = "mkdir " + direc
    print cmd

    for c in xrange(len(cams)):
        cmd = "mkdir " + direc + "cam" + str(c) + "/"
        print cmd


def snap(filename="test.jpg", direc="./"):
    global cams
    cmd = "raspistill -o " + direc + filename
    #os.system(cmd)
    print cmd

    for c in xrange(len(cams)):
        _dir = direc + "cam" + str(c) + "/"
        cmd = "---Camera : " + _dir + filename + ".jpg---"
        print cmd
        #cams[c].start()
        #img = cams[c].get_image()
        #cams[c].stop()
        #pygame.image.save(img, _dir+filename+".jpg")

def check_for_webcams():
    pygame.camera.init()
    return (pygame.camera.list_cameras() == [])
