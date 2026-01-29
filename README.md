# Crashtropolis

A high-octane **Tron-like 2D arcade simulation** where two players battle for survival. Inspired by the classic light cycle mechanics, players must navigate a grid-based arena, cutting off their opponents while avoiding walls and their own trails.

![Crashtropolis](assets/images/red-car.png)

## Features
-   **Local Multiplayer:** 2-player competitive gameplay on a shared screen.
-   **Classic Mechanics:** Navigate grid-based arenas and cut off your opponent.
-   **Audio/Visuals:** Includes custom sprites, background music, and sound effects.

## Controls

### General
-   **SPACE:** Start Game / Restart (from Title or Game Over screen)
-   **ESC / Q:** Quit Game

### Player 1 (Red)
-   **Movement:** Arrow Keys (⬆️ ⬇️ ⬅️ ➡️)

### Player 2 (Blue)
-   **Movement:** WASD (W, A, S, D)

## Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/crashtropolis.git
    cd crashtropolis
    ```

2.  **Install dependencies:**
    This game requires [Pygame](https://www.pygame.org/).
    ```bash
    pip install pygame
    ```

3.  **Run the game:**
    ```bash
    python main.py
    ```

## Project Structure
-   `main.py`: The entry point and main game loop.
-   `player.py`: Player class handling movement and state.
-   `cell.py` / `constants.py`: Game logic and configuration.
-   `assets/`: Contains all images and sound files.
