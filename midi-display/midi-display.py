import pygame, sys, time
import pygame.midi
from pygame.locals import *

import midiInput

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
    #print(pygame.font.get_default_font())


#calculate 'the number'
def calcNumber():
    number = 0
    for index in range(128):
        if midi.midiData[index] > 0:
            number += 2 ** (index % 16)
    number %= 100000
    return number


#calculate the velocity color
def calcColor():
    color = 0
    keyCounter = 0
    for index in range(128):
        if midi.midiData[index] > 0:
            keyCounter += 1
            color += midi.midiData[index] * 2
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
    midi = midiInput.MidiInput()
    midi.open()
    #loopCounter = 0
    old_number = 0
    new_number = 0
    while True:
        time.sleep(0.1)
        checkForExit()
        if midi.connected:
            midi.readData()
        new_number = calcNumber()
        if new_number != old_number:
            DISPLAYSURFACE.fill((0,0,0))
            if new_number != 0:
                #displayText = BIGFONT.render(str(loopCounter).zfill(5), True, (255, 255, 255), (0, 0, 0))
                displayText = BIGFONT.render(str(new_number).zfill(5), True, calcColor(), (0, 0, 0))
                displayRect = displayText.get_rect()
                displayRect.center = (DISPLAYWIDTH // 2, DISPLAYHEIGHT // 2)
                DISPLAYSURFACE.blit(displayText, displayRect)
            old_number = new_number
        pygame.display.update()
        #loopCounter += 1
    