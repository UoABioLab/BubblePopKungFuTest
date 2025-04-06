# Setup Python ----------------------------------------------- #
import pygame
import sys
import os
import color
from settings import *
from game import Game
from menu import Menu
from difficulty import Difficulty
from relative_path import resource_path
from countdown import CountdownScreen


# Setup pygame/window --------------------------------------------- #
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,32) # windows position
pygame.init()
pygame.display.set_caption(WINDOW_NAME)
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),0,32)

mainClock = pygame.time.Clock()

# Fonts ----------------------------------------------------------- #
fps_font = pygame.font.SysFont("coopbl", 22)

# Music ----------------------------------------------------------- #
pygame.mixer.music.load(resource_path("Assets\kung_fu_music.mp3"))
pygame.mixer.music.set_volume(MUSIC_VOLUME)
pygame.mixer.music.play(-1)

# Variables ------------------------------------------------------- #
state = "menu"
LEVEL = None
USER_ID = None
game = None  # Initialize game as None
#countdown_screen = None # Add variable to store countdown_screen instance

# Creation -------------------------------------------------------- #

menu = Menu(SCREEN)
game = Game(SCREEN) # Added from Star Catcher
#countdown_screen = CountdownScreen(SCREEN, 5, game.cap, SCREEN_HEIGHT)  # Pass SCREEN_HEIGHT

# Functions ------------------------------------------------------ #
def user_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

#def clear_events():
#    pygame.event.clear()  # Clear all events

def update():
    global state, game, LEVEL, USER_ID, difficulty_settings, countdown_screen
    
    try:
        if state == "menu":
            menu_result = menu.update()
            if menu_result == "game":

            #     state = "countdown"  # Transition to countdown state
            #     countdown_screen = CountdownScreen(SCREEN, 5, game.cap, SCREEN_HEIGHT)  # Initialize countdown screen with 5 seconds
            #     countdown_screen.start()
            # elif menu_result == "difficulty":
            #     state = "difficulty"
                if 'game' in globals():
                    #game.reset()  # reset the game to start a new game
                    global LIVES
                    LIVES = 3
                    state = "game"
                    #clear_events()  # Clear events when transitioning to a new state
                else:
                    state = "difficulty"  # Go to difficulty selection if game hasn't been initialized yet
            elif menu_result == "difficulty":
                 state = "difficulty"
# #               #clear_events()  # Clear events when transitioning to a new state
        
        elif state == "difficulty":
            
            difficulty_manager = Difficulty(SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT)
            difficulty_manager.show_difficulty_screen()
            LEVEL = difficulty_manager.difficulty
            USER_ID = difficulty_manager.get_user_id()
            #print(f"Main: Received difficulty settings: {difficulty_settings}")
            print(f"Main: LEVEL = {LEVEL}, USER_ID = {USER_ID}")
            # Add new code from star catcher
            #if settings:
            if LEVEL and USER_ID:
                print(f"Selected difficulty: {LEVEL}") #difficulty_manager.difficulty
                print(f"User name is: {USER_ID}")
                #global game
                game = Game(SCREEN, USER_ID, LEVEL)  # Recreate the game instance with new parameters
                game.apply_difficulty_settings(settings)

                state = "menu"  # Change state to menu immediately after selection
                game.reset()
               #pygame.event.clear()  # Clear any pending events

        elif state == "countdown":
            # Handle countdown screen update
            if countdown_screen and countdown_screen.update():
                # Countdown finished, start the game
                state = "game"

        elif state == "game":
            # Added from STar Catcher
            if game is None:
                game = Game(SCREEN, USER_ID, LEVEL)
            #game.reset()

            game_result = game.update()
            if game_result == "menu":
                state = "menu"
                #clear_events()  # Clear events when transitioning to a new state
            elif game_result == "game_over": 
                print("Game Over!")
                state = "menu"
                #clear_events()  # Clear events when transitioning to a new state
            

        pygame.display.update()
        mainClock.tick(FPS)

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit()


# Loop ------------------------------------------------------------ #
while True:

    # Buttons ----------------------------------------------------- #
    user_events()

    # Update ------------------------------------------------------ #
    update()

    # FPS
    if DRAW_FPS:
        fps_label = fps_font.render(f"FPS: {int(mainClock.get_fps())}", 1, (255,200,20))
        SCREEN.blit(fps_label, (5,5))
