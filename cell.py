# Jacob Cardon
# CS1400 - MWF - 8:30am

from pygame import Surface
from constants import *

class Cell:
    """
    Represents one cell in the game grid.
    Each cell can either be empty or contain a laser trail segment.
    """
    __row: int
    __col: int
    __laser: Surface | None

    def __init__(self, row: int, col: int):
        self.__row = row
        self.__col = col
        self.__laser: Surface | None = None   # Starts empty (no trail)

    def has_laser(self) -> bool:
        """Returns True if this cell contains a laser trail."""
        return self.__laser is not None

    def set_laser(self, laser_image: Surface):
        """Places a laser trail image in this cell."""
        self.__laser = laser_image

    def draw(self, screen: Surface):
        """Draws the laser trail (if any) at the correct grid position."""
        if self.__laser:
            # Top-left corner of the cell in screen pixels
            pos_x = self.__row * CELL_SIZE
            pos_y = self.__col * CELL_SIZE
            screen.blit(self.__laser, (pos_x, pos_y))