import pygame, sys, time
import pygame.midi
from pygame.locals import *

#configuration constants
FULLSCREEN = False


#initialization
def init():
    #initialize screen
    global DISPLAYSURFACE, BIGFONT, DISPLAYHEIGHT, DISPLAYWIDTH
    pygame.init()
    if FULLSCREEN:
        DISPLAYSURFACE = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        DISPLAYSURFACE = pygame.display.set_mode((1024, 768))
    DISPLAYWIDTH = DISPLAYSURFACE.get_width()
    DISPLAYHEIGHT = DISPLAYSURFACE.get_height()
    BIGFONT = pygame.font.Font('freesansbold.ttf', DISPLAYHEIGHT // 5)
    print(pygame.font.get_default_font())
    #initialize midi
    global MIDIDATA, MIDIACTIVE, MIDIDEVICE
    pygame.midi.init()
    midiDeviceCount = pygame.midi.get_count()
    #for i in range(midiDeviceCount):
    #        print (pygame.midi.get_device_info(i))
    defaultInputId = pygame.midi.get_default_input_id()
    if defaultInputId >= 0:
        print (pygame.midi.get_device_info(defaultInputId))
        MIDIDEVICE = pygame.midi.Input(defaultInputId)
        MIDIACTIVE = True
    else:
        print("ERROR: no midi device found!")
        MIDIACTIVE = False
    MIDIDATA = []
    for index in range(128):
        MIDIDATA.append(0)
    #MIDIDATA[127] = 63
        

#main application loop
def main():
    #loopCounter = 0
    old_number = 0
    new_number = 0
    while True:
        time.sleep(0.1)
        checkForExit()
        if MIDIACTIVE:
            readMidiInput()
        new_number = calcNumber()
        if new_number != old_number:
            DISPLAYSURFACE.fill((0,0,0))
            if new_number != 0:
                #displayText = BIGFONT.render(str(loopCounter).zfill(5), True, calcColor(), (0, 0, 0))
                displayText = BIGFONT.render(str(new_number).zfill(5), True, (255, 255, 255), (0, 0, 0))
                displayRect = displayText.get_rect()
                displayRect.center = (DISPLAYWIDTH // 2, DISPLAYHEIGHT // 2)
                DISPLAYSURFACE.blit(displayText, displayRect)
            old_number = new_number
        pygame.display.update()
        #loopCounter += 1


#read midi input
def readMidiInput():
    midiInputData = []
    while MIDIDEVICE.poll():
        midiInputData.append(MIDIDEVICE.read(1))
    if midiInputData != []:
        #print (midiInputData)
        for message in midiInputData:
            print (message)
            if len(message) > 0:
                if len(message[0]) > 0:
                    status = message[0][0][0] & 240
                    key = message[0][0][1]
                    velocity = message[0][0][2]
                    print ("status: {}, key: {}, velocity: {}".format(status, key, velocity))
                    MIDIDATA[key] = velocity


#calculate 'the number'
def calcNumber():
    number = 0
    for index in range(128):
        if MIDIDATA[index] > 0:
            number += 2 ** (index % 16)
    number %= 100000
    return number


#calculate the velocity color
def calcColor():
    color = 0
    keyCounter = 0
    for index in range(128):
        if MIDIDATA[index] > 0:
            keyCounter += 1
            color += MIDIDATA[index] * 2
    print (keyCounter)
    if keyCounter == 0:
        return (0, 0, 0)
    color = color // keyCounter
    color = min(color, 255)
    print (color)
    return (color, color, color)


#exit application
def checkForExit():
    for event in pygame.event.get(KEYUP):
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
                

#run application loop
if __name__ == '__main__':
    init()
    main()
    