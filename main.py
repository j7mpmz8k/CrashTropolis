# Jacob Cardon
# CS1400 - MWF - 8:30am

import pygame
from pygame.mixer import music, Sound
from pygame import image
from pygame.transform import scale

from cell import Cell
from constants import *
from player import Player
from message import Message

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    def reset_game():
        nonlocal countdown_timer, winner_msg
        music.fadeout(500)
        countdown_sound.play()
        countdown_timer = 90
        player1.reset()
        player2.reset()
        for row in grid:# Clear all laser trails
            for cell in row:
                cell.set_laser(None)
        winner_msg = None

    ##########
    # Set up game media images, sounds
    ##########
    straight_red = image.load("assets/images/red-straight.png").convert_alpha()
    corner_red   = image.load("assets/images/red-corner.png").convert_alpha()
    straight_blue = image.load("assets/images/blue-straight.png").convert_alpha()
    corner_blue   = image.load("assets/images/blue-corner.png").convert_alpha()

    red_car = image.load("assets/images/red-car.png")
    red_car = scale(red_car, (CAR_SIZE, CAR_SIZE))
    blue_car = image.load("assets/images/blue-car.png")
    blue_car = scale(blue_car, (CAR_SIZE, CAR_SIZE))

    background = image.load("assets/images/grid.png")
    background = scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    BG_MUSIC = "assets/sounds/background-music.mp3"
    TITLE_SCREEN_MUSIC = "assets/sounds/titlescreen-music.mp3"
    GAME_OVER_MUSIC = "assets/sounds/gameover-music.wav"
    music.load(TITLE_SCREEN_MUSIC)
    music.set_volume(.75)
    music.play(-1)

    turn1_sound = Sound("assets/sounds/turn-1.mp3")
    turn1_sound.set_volume(.2)
    turn2_sound = Sound("assets/sounds/turn-2.mp3")
    turn2_sound.set_volume(.2)
    crash_sound = Sound("assets/sounds/crash.wav")
    crash_sound.set_volume(.25)
    countdown_sound = Sound("assets/sounds/countdown.mp3")
    countdown_sound.set_volume(.25)

    # Messages
    title_msg       = Message("CRASHTROPOLIS", "purple", "big", "title")
    ready_msg       = Message("READY", "white", "big", "center")
    set_msg         = Message("SET", "white", "big", "center")
    go_msg          = Message("GO!", "green", "big", "center")
    draw_msg        = Message("DRAW!", "purple", "big", "title")
    red_wins_msg    = Message("RED WINS!", "red", "big", "title")
    blue_wins_msg   = Message("BLUE WINS!", "blue", "big", "title")
    press_start_msg = Message("press SPACE bar to play", "white", "small", "press")
    play_again_msg  = Message("press SPACE bar to play again", "white", "small", "press")

    ##########
    # Set up game data
    ##########
    grid = []
    for row in range(GRID_SIZE):
        new_row = []
        for col in range(GRID_SIZE):
            new_row.append(Cell(row, col))
        grid.append(new_row)

    player1 = Player("player1", red_car, straight_red, corner_red, [GRID_SIZE // 3 * 2, GRID_SIZE - 1], turn1_sound)
    player2 = Player("player2", blue_car, straight_blue, corner_blue, [GRID_SIZE // 3, GRID_SIZE - 1], turn2_sound)

    countdown_timer = 0
    winner_msg = None

    ##########
    # Game Loop
    ##########
    title_screen = True
    countdown = False
    playing = False
    game_over = False
    running = True
    while running:
        ##########
        # Get Input/Events
        ##########
        for event in pygame.event.get():
            #exits window
            if event.type == pygame.QUIT:
                running = False
            #checks key presss
            if event.type == pygame.KEYDOWN:
                # quits game
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    running = True
                #restarts game
                if event.key == pygame.K_SPACE and (title_screen or game_over):
                    reset_game()
                    countdown = True
                    title_screen = False
                    game_over = False
                #player movement
                if playing:
                    if event.key   == pygame.K_UP:    player1.set_dir(UP)
                    elif event.key == pygame.K_RIGHT: player1.set_dir(RIGHT)
                    elif event.key == pygame.K_DOWN:  player1.set_dir(DOWN)
                    elif event.key == pygame.K_LEFT:  player1.set_dir(LEFT)

                    if event.key   == pygame.K_w: player2.set_dir(UP)
                    elif event.key == pygame.K_d: player2.set_dir(RIGHT)
                    elif event.key == pygame.K_s: player2.set_dir(DOWN)
                    elif event.key == pygame.K_a: player2.set_dir(LEFT)

        ##########
        # Update state of components/data
        ##########
        #### Always Update ####

        #### Update if Game is Not Over ####
        if countdown:
            countdown_timer -= 1
            if countdown_timer <= 0:
                playing = True
                countdown = False
                music.load(BG_MUSIC)
                music.set_volume(.2)
                music.play(-1)

        if playing:
            p1_crash = player1.would_crash(grid)
            p2_crash = player2.would_crash(grid)

            if p1_crash or p2_crash:
                game_over = True
                playing = False
                crash_sound.play()
                music.fadeout(1000)
                music.load(GAME_OVER_MUSIC)
                music.set_volume(.5)
                music.play(-1)

                if p1_crash and p2_crash:
                    winner_msg = draw_msg
                elif p1_crash:
                    winner_msg = blue_wins_msg
                else:
                    winner_msg = red_wins_msg
            else:
                player1.move(grid)
                player2.move(grid)

        ##########
        # Update Display
        ##########
        #### Always Display ####
        screen.blit(background, (0, 0))

        for row in grid:
            for cell in row:
                cell.draw(screen)

        player1.draw(screen)
        player2.draw(screen)
        #### Display before Game is being played ####
        if title_screen:
            title_msg.draw(screen)
            press_start_msg.draw(screen)
        #### Display when Game is started ####
        elif countdown:
            if countdown_timer > 60:   ready_msg.draw(screen)
            elif countdown_timer > 30: set_msg.draw(screen)
            elif countdown_timer > 0:  go_msg.draw(screen)
        #### Display while Game is Over ####
        elif game_over:
            winner_msg.draw(screen)
            play_again_msg.draw(screen)

        pygame.display.flip()
        clock.tick(CLOCK_TICK)

main()