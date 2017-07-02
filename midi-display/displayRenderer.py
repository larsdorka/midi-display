import pygame


class DisplayRenderer:
    """class to render generated number to the screen"""
    
    def __init__(self, debug_log=dict()):
        self.debug_log = debug_log
        self.full_screen = False
        self.render_zero = False
        self.display_buffer = None
        self.big_font = None
        self.small_font = None
        self.display_width = 0
        self.display_height = 0
        
    def open(self, full_screen=False, render_zero=False):
        """initializes the screen and render objects"""
        self.debug_log['display'] = ""
        self.full_screen = full_screen
        self.render_zero = render_zero
        if self.full_screen:
            self.display_buffer = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.display_buffer = pygame.display.set_mode((1024, 768))
        self.display_width = self.display_buffer.get_width()
        self.display_height = self.display_buffer.get_height()
        self.big_font = pygame.font.Font('freesansbold.ttf', self.display_height // 5)
        self.small_font = pygame.font.Font('freesansbold.ttf', 11)
        self.display_buffer.fill((0, 0, 0))

    def render_state(self):
        """renders connection and error messages as debug information"""
        display_text = self.small_font.render(self.debug_log['midi'], True, (255, 255, 255), (0, 0, 0))
        display_rect = display_text.get_rect()
        self.display_buffer.blit(display_text, display_rect)

    def render_number(self, number, color=(255, 255, 255)):
        """renders a number in a large font in the center of the screen"""
        if number != 0 or self.render_zero is True:
            display_text = self.big_font.render(str(number).zfill(5), True, color, (0, 0, 0))
            display_rect = display_text.get_rect()
            display_rect.center = (self.display_width // 2, self.display_height // 2)
            self.display_buffer.blit(display_text, display_rect)

    def update(self):
        """updates the screen with the current buffer and clears the buffer"""
        pygame.display.update()
        self.display_buffer.fill((0, 0, 0))
