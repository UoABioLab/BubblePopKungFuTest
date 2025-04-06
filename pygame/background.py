import pygame
import image
from settings import *
from relative_path import resource_path


class Background:
    def __init__(self):
        self.image = image.load(resource_path("Assets\dojo.jpg"), size=(SCREEN_WIDTH, SCREEN_HEIGHT),
                                convert="default")


    def draw(self, surface):
        image.draw(surface, self.image, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), pos_mode="center")

        ground_width = SCREEN_WIDTH
        ground_height = 50
        ground_x = 0
        ground_y = SCREEN_HEIGHT - ground_height

        pygame.draw.rect(SCREEN, (255, 255, 255), (ground_x, ground_y, ground_width, ground_height))

       
