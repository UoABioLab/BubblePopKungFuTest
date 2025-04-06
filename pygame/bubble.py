import pygame
import random
import time
import image
from settings import *
from relative_path import resource_path
from difficulty import Difficulty
#from background import *

class Bubble:
    def __init__(self, velocity):
    #def __init__(self):     
        #size
        random_size_value = random.uniform(BUBBLE_SIZE_RANDOMIZE[0], BUBBLE_SIZE_RANDOMIZE[1])
        self.size = (int(BUBBLE_SIZES[0] * random_size_value), int(BUBBLE_SIZES[1] * random_size_value))
        self.rect = pygame.Rect(0, 0, int(self.size[0]//1.4), int(self.size[1]//1.4))
        self.images = [image.load(resource_path("Assets\pink_balloon.png"), size=self.size)]
        #self.vel = self.define_spawn_pos()
        
        self.vel = [0, velocity]
        self.define_spawn_pos()
        
        # movement
        #moving_direction, start_pos = self.define_spawn_pos(size)
        #self.vel = self.define_spawn_pos(size)[1]
        
        # sprite
        #self.rect = pygame.Rect(start_pos[0], start_pos[1], size[0]//1.4, size[1]//1.4)
        #self.images = [image.load("bubble_pop\Assets\pink_balloon.png", size=size, flip=moving_direction=="right")]
        #self.image_pop = [image.load("bubble_pop\Assets\green_pop.png", size=size, flip=moving_direction=="right")]
        self.current_frame = 0
        self.animation_timer = 0

        self.left = False
        self.right = False

        self.spawn_time = time.time()
        self.stationary_duration = 5  # seconds
        self.is_stationary = True
                
        # Print the position when spawned
        print(f"Bubble spawned at position: {self.rect.topleft} with velocity: {velocity}")
    

    #def define_spawn_pos(self, size): # define the start pos and moving vel of the object
    def define_spawn_pos(self):
        
        side = random.randint(1, 2)
        print (side)
        if side == 1:
            self.rect.topleft = (random.randint(400, 450), SCREEN_HEIGHT//2 + 50)
            self.left = True
            self.right = False
        else:
            self.rect.topleft = (random.randint(700, 750), SCREEN_HEIGHT//2 + 50)
            self.left = False
            self.right = True
        
        return [0, self.vel]
        
        #moving_direction = random.choice(("left", "right", "up", "down"))
        #moving_direction = "down"
        # Set the range for dropping objects
        #min_x = 200
        #max_x = 1000
        #if moving_direction == "right":
        #    start_pos = (-size[0], random.randint(size[1], SCREEN_HEIGHT-size[1]))
        #    self.vel = [vel, 0]
        #if moving_direction == "left":
        #    start_pos = (SCREEN_WIDTH + size[0], random.randint(size[1], SCREEN_HEIGHT-size[1]))
        #    self.vel = [-vel, 0]
        #if moving_direction == "up":
        #    start_pos = (random.randint(size[0], SCREEN_WIDTH-size[0]), SCREEN_HEIGHT+size[1])
        #    self.vel = [0, -vel]
        #if moving_direction == "down":
            #start_pos = (random.randint(size[0], SCREEN_WIDTH-size[0]), -size[1])
            #start_pos = (random.randint(MIN_DROP, MAX_DROP - size[0]), -size[1])
            #start_pos = (random.randint(MIN_DROP, MAX_DROP - size[0]), SCREEN_HEIGHT//2)
        #    if side == 1:
        #        start_pos = (random.randint(50, 400), SCREEN_HEIGHT//2)
        #        self.vel = [0, vel]      
        #    else:
        #        start_pos = (random.randint(900, 1150), SCREEN_HEIGHT//2)
        #        self.vel = [0, vel]
        #return moving_direction, start_pos

    def move(self):
    #    self.rect.move_ip(self.vel)
    #    self.rect.y += self.vel[1] # make object go down
        current_time = time.time()
        if current_time - self.spawn_time > self.stationary_duration:
            self.is_stationary = False
            self.rect.y += self.vel[1]  # make object go down rapidly
        
    def animate(self): # change the frame of the insect when needed
        t = time.time()

        if t > self.animation_timer:
            self.animation_timer = t + ANIMATION_SPEED
            self.current_frame += 1
            
            if self.current_frame > len(self.images)-1:
                self.current_frame = 0

    def draw_hitbox(self, surface):
        pygame.draw.rect(surface, (200, 60, 0), self.rect)

    def draw(self, surface):
        #self.animate()
        #image.draw(surface, self.images[self.current_frame], self.rect.center, pos_mode="center")       
        image.draw(surface, self.images[0], self.rect.center, pos_mode="center")

        if DRAW_HITBOX:
            self.draw_hitbox(surface)

    def hit_floor(self):
        return self.rect.bottom >= FLOOR

    def kill(self, bubbles): # remove the object from the list
        if self in bubbles:
            bubbles.remove(self)
            return 2
    
    #def can_be_popped(self, player_leg_up_time):
    #    return self.is_stationary and player_leg_up_time >= 2

