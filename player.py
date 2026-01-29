# Jacob Cardon
# CS1400 - MWF - 8:30am
from pygame import Surface, Rect
from pygame.transform import rotate
from pygame.mixer import Sound

from cell import Cell
from constants import *

class Player:
    """
    Represents one player (car) in the game.
    Handles movement, trail drawing, direction changes, crash detection, and rendering.
    """
    __name: str
    __alive: bool#currently does nothing
    __reset_pos: list[int]              # Starting grid position for reset
    __grid_pos: list[int]               # Current grid position [row, col]
    __previous_grid_pos: list[int]      # Position from the previous frame
    __car_rect: Rect                    # Rectangle used for drawing the car
    __old_dir: tuple[int,int]           # Current movement direction
    __old_dir: tuple[int,int]           # Direction in the previous frame (for corner detection)
    __car_images: list[Surface]         # Pre-rotated car images [UP, RIGHT, DOWN, LEFT]
    __straight_laser_images: list[Surface]
    __corner_laser_images: list[Surface]
    __turn_sound: Sound

    def __init__(self, name, car: Surface, laser: Surface, corner_laser: Surface, grid_pos: list[int], turn_sound: Sound):
        self.__name = name
        self.__alive = True
        self.__reset_pos = grid_pos
        self.__grid_pos = grid_pos
        self.__previous_grid_pos = grid_pos

        # Position car rect in the center of its starting cell
        self.__car_rect = car.get_rect(center=(
            (grid_pos[0] * CELL_SIZE + CELL_SIZE // 2),
            (grid_pos[1] * CELL_SIZE + CELL_SIZE // 2)
        ))

        self.__dir = UP
        self.__old_dir = UP

        # Pre-rotate car images for each direction (faster than rotating every frame)
        self.__car_images = [
            car,                   # UP
            rotate(car, -90),      # RIGHT
            rotate(car, 180),      # DOWN
            rotate(car, 90),       # LEFT
        ]

        # Pre-rotate straight laser trail images
        self.__straight_laser_images = [
            laser,                  # UP / DOWN (same image, vertical)
            rotate(laser, 90),      # RIGHT / LEFT (rotated to horizontal)
            laser,                  # DOWN (same as UP)
            rotate(laser, 90),      # LEFT (same as RIGHT)
        ]

        # Pre-rotate corner laser pieces (used when player turns)
        self.__corner_laser_images = [
            corner_laser,                  # left→down or up→right
            rotate(corner_laser, 90),      # left→up or down→right
            rotate(corner_laser, 180),     # right→up or down→left
            rotate(corner_laser, 270),     # right→down or up→left
        ]

        self.__turn_sound = turn_sound

    def __get_laser_image(self):
        """Returns the correct laser image (straight or corner) based on previous and current direction."""
        if self.__old_dir == self.__dir:
            return self.__straight_laser_images[DIR_LST.index(self.__dir)]
        elif (self.__old_dir == LEFT and self.__dir == DOWN) or (self.__old_dir == UP and self.__dir == RIGHT):
            return self.__corner_laser_images[0]
        elif (self.__old_dir == LEFT and self.__dir == UP) or (self.__old_dir == DOWN and self.__dir == RIGHT):
            return self.__corner_laser_images[1]
        elif (self.__old_dir == RIGHT and self.__dir == UP) or (self.__old_dir == DOWN and self.__dir == LEFT):
            return self.__corner_laser_images[2]
        elif (self.__old_dir == RIGHT and self.__dir == DOWN) or (self.__old_dir == UP and self.__dir == LEFT):
            return self.__corner_laser_images[3]
        else:
            return None

    def __get_car_image(self):
        """Returns the correctly rotated car image for the current direction."""
        for i, dir in enumerate(DIR_LST):
            if self.__dir == dir:
                return self.__car_images[i]

    def __play_turn_sound(self):
        """Plays the turn sound effect (called only when direction actually changes)."""
        self.__turn_sound.play()

    def set_dir(self, new_dir: tuple[int,int]):
        """Changes direction only if the new direction is not the direct opposite (prevents instant reversal)."""
        opposite = (-self.__dir[0], -self.__dir[1])
        if new_dir != opposite:
            self.__dir = new_dir
            self.__play_turn_sound()

    def would_crash(self, grid: list[list[Cell]]) -> bool:
        """
        Checks if the next move would cause a crash (wall or existing laser).
        Returns True if crash would occur.
        """
        new_row = self.__grid_pos[0] + self.__dir[0]
        new_col = self.__grid_pos[1] + self.__dir[1]

        # Wall collision
        if not (0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE):
            self.__alive = False
            return True

        # Laser trail collision
        if grid[new_row][new_col].has_laser():
            self.__alive = False
            return True

        return False

    def move(self, grid: list[list[Cell]]):
        """Moves the player one cell forward and draws the appropriate laser trail segment behind."""
        self.__previous_grid_pos = self.__grid_pos[:]
        prev_row = self.__previous_grid_pos[0]
        prev_col = self.__previous_grid_pos[1]

        # Draw laser trail in the cell we are leaving
        grid[prev_row][prev_col].set_laser(self.__get_laser_image())

        # Update grid position
        for i in range(len(self.__dir)):
            self.__grid_pos[i] += self.__dir[i]

        # Update old direction for next frame's corner detection
        self.__old_dir = self.__dir

    def draw(self, screen: Surface):
        """Draws the car at its current grid position with correct rotation."""
        self.__car_rect.center = (
            self.__grid_pos[0] * CELL_SIZE + CELL_SIZE // 2,
            self.__grid_pos[1] * CELL_SIZE + CELL_SIZE // 2
        )
        image = self.__get_car_image()
        screen.blit(image, self.__car_rect.topleft)

    def reset(self):
        """Resets player to starting position and direction (used at the start of each round)."""
        self.__grid_pos = self.__reset_pos[:]
        self.__dir = UP
        self.__old_dir = UP
        self.__alive = True