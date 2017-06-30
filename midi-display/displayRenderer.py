import pygame
from pygame.locals import *

class DisplayRenderer:
    '''class to render generated number to the screen'''
    
    def __init__(self):
        self.fullscreen = False
        self.renderZero = False
        self.displaySurface = None
        self.bigFont = None
        self.displayWidth = 0
        self.displayHeight = 0

        
    def open(self, fullscreen = False, renderZero = False):
        self.fullscreen = fullscreen
        self.renderZero = renderZero
        if self.fullscreen:
            self.displaySurface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.displaySurface = pygame.display.set_mode((1024, 768))
        self.displayWidth = self.displaySurface.get_width()
        self.displayHeight = self.displaySurface.get_height()
        self.bigFont = pygame.font.Font('freesansbold.ttf', self.displayHeight // 5)
    
    
    def renderNumber(self, number, color = (255, 255, 255)):
        self.displaySurface.fill((0,0,0))
        if number != 0 or self.renderZero == True:
            displayText = self.bigFont.render(str(number).zfill(5), True, color, (0, 0, 0))
            displayRect = displayText.get_rect()
            displayRect.center = (self.displayWidth // 2, self.displayHeight // 2)
            self.displaySurface.blit(displayText, displayRect)
        pygame.display.update()
