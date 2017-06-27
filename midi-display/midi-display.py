import pygame, sys, time
from pygame.locals import *


#initilization
def init():
    global DISPLAYSURFACE, BIGFONT
    pygame.init()
    DISPLAYSURFACE = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 200)
    print(pygame.font.get_default_font())
    global MIDIDATA
    MIDIDATA = []
    for index in range(128):
        MIDIDATA.append(0)
    MIDIDATA[127] = 63
        

#main application loop
def main():
    loopCounter = 0
    old_number = 0
    new_number = 0
    while True:
        time.sleep(0.1)
        checkForExit()
        new_number = calcNumber()
        if new_number != old_number:
            DISPLAYSURFACE.fill((0,0,0))
            if new_number != 0:
                displayText = BIGFONT.render(str(loopCounter).zfill(5), True, calcColor(), (0,0,0))
                #displayText = BIGFONT.render(str(new_number).zfill(5), True, (255,255,255), (0,0,0))
                displayRect = displayText.get_rect()
                displayRect.center = (960,540)
                DISPLAYSURFACE.blit(displayText, displayRect)
            old_number = new_number
        pygame.display.update()
        loopCounter += 1


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
