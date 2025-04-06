import pygame
import random
import image
from settings import *
from bubble import Bubble
from relative_path import resource_path

class Balloon(Bubble):
    def __init__(self):
        #size
        #random_size_value = random.uniform(BALLOON_SIZE_RANDOMIZE[0], BALLOON_SIZE_RANDOMIZE[1])
        #size = (int(BALLOON_SIZES[0] * random_size_value), int(BALLOON_SIZES[1] * random_size_value))
        #moving_direction, start_pos = self.define_spawn_pos(size)
        #self.rect = pygame.Rect(start_pos[0], start_pos[1], size[0]//1.4, size[1]//1.4)
        #self.images = [image.load(f"star_catcher/Assets/star/{nb}.png", size=size, flip=moving_direction=="right") for nb in range(1, 7)] # load the multiple images of twinkling star to simulate animation
        super().__init__()  # Call the parent class constructor
        self.images = [image.load(resource_path("Assets\green_balloon.png"), size=self.size)]
        print(f"Balloon spawned at position: {self.rect.topleft}")
        self.current_frame = 0
        self.animation_timer = 0
    
    def animate(self):
        # Balloons don't animate, so we can leave this empty or add a simple animation if desired
        pass

    def draw(self, surface):
        image.draw(surface, self.images[0], self.rect.center, pos_mode="center")
        #print(f"Balloon at position: {self.rect.topleft}")
        if DRAW_HITBOX:
            self.draw_hitbox(surface)

    def hit_floor(self):
        return self.rect.bottom >= FLOOR

    def kill(self, bubbles): # remove the object from the list
        bubbles.remove(self)
        return 5
    
    
