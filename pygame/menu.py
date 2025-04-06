import pygame
import sys
from settings import *
from background import Background
import UI
from relative_path import resource_path


class Menu:
    def __init__(self, surface):
        self.surface = surface
        self.background = Background()
        self.click_sound = pygame.mixer.Sound(resource_path("Assets\pop_sound.mp3"))
        self.confirm_quit = False  # Add a flag for quit confirmation


    def draw(self):
        self.background.draw(self.surface)
        # draw title
        UI.draw_text(self.surface, GAME_TITLE, (SCREEN_WIDTH//2, 120), (255,255,255), font=FONTS["big"],
                    shadow=True, shadow_color=(0, 0, 0), pos_mode="center")
        UI.draw_text(self.surface, "How to play the game:", (SCREEN_WIDTH - 770, 200), (255, 255, 255), font=FONTS["medium"],
                    shadow=True, shadow_color=(0, 0, 0))
        UI.draw_text(self.surface, "1.Choose difficulty level.", (SCREEN_WIDTH - 770, 280), (255, 255, 255), font=FONTS["medium"],
                    shadow=True, shadow_color=(0, 0, 0))
        UI.draw_text(self.surface, "2.Left foot for left balloons.", (SCREEN_WIDTH - 770, 360), (255, 255, 255), font=FONTS["medium"],
                    shadow=True, shadow_color=(0, 0, 0))
        UI.draw_text(self.surface, "3.Right foot for right balloons", (SCREEN_WIDTH - 770, 440), (255, 255, 255), font=FONTS["medium"],
                    shadow=True, shadow_color=(0, 0, 0))
        UI.draw_text(self.surface, "4.Don't let balloons hit the floor.", (SCREEN_WIDTH - 770, 520), (255, 255, 255), font=FONTS["medium"],
                    shadow=True, shadow_color=(0, 0, 0))
        UI.draw_text(self.surface, "5.Have fun.", (SCREEN_WIDTH - 770, 600), (255, 255, 255), font=FONTS["medium"],
                    shadow=True, shadow_color=(0, 0, 0))


    def update(self):
        self.draw()
        #if UI.button(self.surface, (SCREEN_WIDTH // 2, 250), "START", click_sound=self.click_sound):
        if UI.button(self.surface, (100, 250), "START", click_sound=self.click_sound):
            return "game"
        
        #if UI.button(self.surface, (SCREEN_WIDTH // 2, 250+BUTTONS_SIZES[1]*1.5), "DIFFICULTY", click_sound=self.click_sound):
        if UI.button(self.surface, (100, 250+BUTTONS_SIZES[1]*1.5), "DIFFICULTY", click_sound=self.click_sound):
            return "difficulty"

        #if UI.button(self.surface, (SCREEN_WIDTH // 2, 250+BUTTONS_SIZES[1]*3), "QUIT", click_sound=self.click_sound):
        if UI.button(self.surface, (100, 250+BUTTONS_SIZES[1]*3), "QUIT", click_sound=self.click_sound):
            pygame.quit()
            sys.exit()

        #elif UI.button(self.surface, 250+BUTTONS_SIZES[1]*4, "CANCEL", click_sound=self.click_sound):
        #        self.confirm_quit = False
        #else:
        #    if UI.button(self.surface, 250+BUTTONS_SIZES[1]*3, "QUIT", click_sound=self.click_sound):
        #        self.confirm_quit = True  # Set confirmation flag

        