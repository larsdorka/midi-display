import pygame, sys, time
from pygame.locals import *


#initilization
def init():
    global DISPLAYSURFACE, BIGFONT
    pygame.init()
    DISPLAYSURFACE = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 200)


#main application loop
def main():
    counter = 0
    while True:
        time.sleep(0.1)
        for event in pygame.event.get(KEYUP):
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        DISPLAYSURFACE.fill((0,0,0)) 
        displayText = BIGFONT.render(str(counter), True, (255,255,255), (0,0,0))
        displayRect = displayText.get_rect()
        displayRect.center = (960,540)
        DISPLAYSURFACE.blit(displayText, displayRect)
        pygame.display.update()
        counter += 1


#run application loop
if __name__ == '__main__':
    init()
    main()
