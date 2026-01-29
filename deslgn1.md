## Cell

**Attributes**

| Visibility | Name  | Type            |
|------------|-------|-----------------|
| -          | row   | int             |
| -          | col   | int             |
| -          | laser | Surface \| None |

**Methods**

| Visibility | Method          | Parameters                          | Returns   |
|------------|-----------------|-------------------------------------|-----------|
| +          | __init__        | row: int, col: int                  | None      |
| +          | has_laser       | ()                                  | bool      |
| +          | set_laser       | laser_image: Surface \| None        | None      |
| +          | draw            | screen: Surface                     | None      |


***
## Player

**Attributes**

| Visibility | Name                  | Type           |
|------------|-----------------------|----------------|
| -          | name                  | str            |
| -          | alive                 | bool           |
| -          | reset_pos             | list[int]      |
| -          | grid_pos              | list[int]      |
| -          | previous_grid_pos     | list[int]      |
| -          | car_rect              | Rect           |
| -          | dir                   | tuple[int,int] |
| -          | old_dir               | tuple[int,int] |
| -          | car_images            | list[Surface]  |
| -          | straight_laser_images | list[Surface]  |
| -          | corner_laser_images   | list[Surface]  |
| -          | turn_sound            | Sound          |

**Methods**

| Visibility | Method          | Parameters                                                                                             | Returns         |
|------------|-----------------|--------------------------------------------------------------------------------------------------------|-----------------|
| +          | __init__        | name: str, car: Surface, laser: Surface, corner_laser: Surface, grid_pos: list[int], turn_sound: Sound | None            |
| -          | get_laser_image | ()                                                                                                     | Surface \| None |
| -          | get_car_image   | ()                                                                                                     | Surface         |
| -          | play_turn_sound | ()                                                                                                     | None            |
| +          | set_dir         | new_dir: tuple[int,int]                                                                                | None            |
| +          | would_crash     | grid: list[list[Cell]]                                                                                 | bool            |
| +          | move            | grid: list[list[Cell]]                                                                                 | None            |
| +          | draw            | screen: Surface                                                                                        | None            |
| +          | reset           | ()                                                                                                     | None            |

***
## Message

**Attributes**

| Visibility | Name            | Type             |
|------------|-----------------|------------------|
| -          | font            | pygame.font.Font |
| -          | surface         | Surface          |
| -          | rect            | Rect             |
| -          | position_type   | str              |

**Methods**

| Visibility | Method   | Parameters                                                                       | Returns |
|------------|----------|----------------------------------------------------------------------------------|---------|
| +          | __init__ | text: str, color: str \| tuple, size: str = "big", position_type: str = "center" | None    |
| +          | draw     | screen: Surface                                                                  | None    |



Main game loop:

    1. Check User Inputs / Events

       - Player closes the window -> stop running
       - Player presses Q or Escape -> stop running (currently commented out)
       - Game is on title screen or game over screen and player presses Spacebar -> start/restart round:
           - Play countdown sound
           - Reset countdown_timer to 90
           - Reset both players to starting positions and direction (UP)
           - Clear every laser trail from all 80×80 cells
           - Set winner_msg to None
           - Switch to countdown mode (countdown = True, others False)
       - If the game is actively playing:
           - Arrow keys -> Player 1 changes direction (UP/RIGHT/DOWN/LEFT), only if not direct reverse
           - WASD keys     -> Player 2 changes direction (W=UP, D=RIGHT, S=DOWN, A=LEFT), only if not direct reverse
           - When direction actually changes -> play turn sound

    2. Update Game State

       - If in countdown mode:
           - Decrease countdown_timer by 1
           - When timer reaches 0 -> switch to playing mode, load and play background music

       - If playing game:
           - Check if Player 1 would crash on next move
           - Check if Player 2 would crash on next move
           - If either or both would crash:
               - Switch to game over state
               - Play crash sound
               - Fade out music, then play game-over music
               - Set winner_msg:
                   both crash -> "DRAW!"
                   only red crashes -> "BLUE WINS!"
                   only blue crashes -> "RED WINS!"
           - If no crash -> both players move forward one cell and leave correct laser trail (straight or corner) behind them

    3. Update Display

       - Always draw the full-size background image first
       - Draw every laser trail segment in every cell that has one
       - Draw both cars on top of the trails (cars are always visible on top)
       
       - If on title screen -> draw "CRASHTROPOLIS" title and "press SPACE bar to play"
       - If in countdown:
           - timer > 60 -> draw "READY"
           - timer > 30 -> draw "SET"
           - timer > 0  -> draw "GO!"
       - If game is over -> draw the winner/draw message and "press SPACE bar to play again"