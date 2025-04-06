import pygame

class Settings:
    def __init__(self):
        self.MIN_DROP = 400
        self.MAX_DROP = 750
        self.SPAWN_TIME = 7
        self.VELOCITY = 3
        self.LEG_UP_TIME = 2

settings = Settings()

def update_difficulty_settings(new_spawn_time, new_velocity, new_leg_up_time):
    print(f"Settings: Updating with new_leg_up_time = {new_leg_up_time}")
    settings.SPAWN_TIME = new_spawn_time
    settings.VELOCITY = new_velocity
    settings.LEG_UP_TIME = new_leg_up_time
    print(f"Settings: Updated: LEG_UP_TIME={settings.LEG_UP_TIME}")

WINDOW_NAME = "Bubble Pop"
GAME_TITLE = WINDOW_NAME

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),0,32)

FPS = 90
DRAW_FPS = True

# sizes
BUTTONS_SIZES = (300, 90)
PLAYER_SIZE = 500
PLAYER_HITBOX_SIZE = (300, 300)
BUBBLE_SIZES = (50, 50)
BUBBLE_SIZE_RANDOMIZE = (1.2,1.5)
BALLOON_SIZES = (50, 50)
BALLOON_SIZE_RANDOMIZE = (1.2, 1.5)
SIZE_MULTIPLIER = 0.9

# drawing
DRAW_HITBOX = False # will draw all the hitbox
FLOOR = 650


# animation
ANIMATION_SPEED = 0.08 # the frame of the objects will change every X sec


# difficulty
GAME_DURATION = 60 # the game will last X sec

# Default values
LIVES = 3
BUBBLE_MOVE_SPEED = {"min": 1, "max": 3}  
MIN_DROP = 200
MAX_DROP = 1000
BUBBLE_SPAWN_TIME = 5
POSITION_FACTOR = 2

# colors
COLORS = {"title": (255, 220, 0), "score": (255, 220, 0), "timer": (255, 220, 0),
            "buttons": {"default": (56, 67, 209), "second":  (87, 99, 255),
                        "text": (255, 255, 255), "gray": (38, 61, 39), "shadow": (46, 54, 163)}} # second is the color when the mouse is on the button
#Gold = (255, 220, 0)
#Gray = (38, 61, 39)

# sounds / music
MUSIC_VOLUME = 0.5 # value between 0 and 1
SOUNDS_VOLUME = 3

# fonts
pygame.font.init()
FONTS = {}
FONTS["small"] = pygame.font.Font(None, 40)
FONTS["medium"] = pygame.font.Font(None, 72)
FONTS["big"] = pygame.font.Font(None, 120)

