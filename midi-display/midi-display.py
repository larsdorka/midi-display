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
    #MIDIDATA[127] = 1
        

#main application loop
def main():
    #counter = 0
    old_number = 0
    new_number = 0
    while True:
        time.sleep(0.1)
        for event in pygame.event.get(KEYUP):
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        new_number = calcNumber()
        if new_number != old_number:
            DISPLAYSURFACE.fill((0,0,0))
            if new_number != 0:
                #displayText = BIGFONT.render(str(counter).zfill(5), True, (255,255,255), (0,0,0))
                displayText = BIGFONT.render(str(new_number).zfill(5), True, (255,255,255), (0,0,0))
                displayRect = displayText.get_rect()
                displayRect.center = (960,540)
                DISPLAYSURFACE.blit(displayText, displayRect)
            old_number = new_number
        pygame.display.update()
        #counter += 1


#calculate 'the number'
def calcNumber():
    number = 0
    for index in range(128):
        if MIDIDATA[index] > 0:
            number += 2 ** (index % 16)
    number %= 100000
    return number


#run application loop
if __name__ == '__main__':
    init()
    main()
