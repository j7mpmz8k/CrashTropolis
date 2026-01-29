# Jacob Cardon
# CS1400 - MWF - 8:30am
import pygame
from pygame import Surface, Rect

from constants import *

class Message:
    """
    Handles rendering centered text messages (title, READY/SET/GO, win messages, etc.)
    """
    __font: pygame.font.Font
    __surface: Surface
    __rect: Rect
    __position_type: str
    def __init__(self, text: str, color, size: str = "big", position_type: str = "center"):
        # Calculate common positions
        center_x, center_y = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        title_y_offset = int(SCREEN_HEIGHT * 0.12)   # Moves title up a bit
        press_y_offset = int(SCREEN_HEIGHT * 0.18)   # Moves "press space" down

        # Font selection - big for titles, small for instructions
        big_font = pygame.font.SysFont("impact", int(SCREEN_HEIGHT * 0.15), bold=True)
        small_font = pygame.font.SysFont("arial", int(SCREEN_HEIGHT * 0.0625))
        self.__font = big_font if size == "big" else small_font

        # Render the text surface
        self.__surface = self.__font.render(text, True, color)
        self.__rect = self.__surface.get_rect()

        # Position the message based on type
        self.__position_type = position_type
        if position_type == "title":          # Title and winner screens
            self.__rect.center = (center_x, center_y - title_y_offset)
        elif position_type == "press":        # "press SPACE bar" prompts
            self.__rect.center = (center_x, center_y + press_y_offset)
        elif position_type == "center":       # READY / SET / GO!
            self.__rect.center = (center_x, center_y)

    def draw(self, screen):
        """Blits the message to the screen."""
        screen.blit(self.__surface, self.__rect)