import pygame


class DisplayRenderer:
    """class to render generated number to the screen"""
    
    def __init__(self):
        self.full_screen = False
        self.render_zero = False
        self.display_surface = None
        self.big_font = None
        self.display_width = 0
        self.display_height = 0
        
    def open(self, full_screen=False, render_zero=False):
        self.full_screen = full_screen
        self.render_zero = render_zero
        if self.full_screen:
            self.display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.display_surface = pygame.display.set_mode((1024, 768))
        self.display_width = self.display_surface.get_width()
        self.display_height = self.display_surface.get_height()
        self.big_font = pygame.font.Font('freesansbold.ttf', self.display_height // 5)
    
    def render_number(self, number, color=(255, 255, 255)):
        self.display_surface.fill((0, 0, 0))
        if number != 0 or self.render_zero is True:
            display_text = self.big_font.render(str(number).zfill(5), True, color, (0, 0, 0))
            display_rect = display_text.get_rect()
            display_rect.center = (self.display_width // 2, self.display_height // 2)
            self.display_surface.blit(display_text, display_rect)
        pygame.display.update()
