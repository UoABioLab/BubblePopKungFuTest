import pygame
import image
import time
from settings import *
from pose_tracking import PoseTracking
from bubble import Bubble
import cv2
from relative_path import resource_path

class Player:
    def __init__(self):
        self.orig_image = image.load(resource_path("Assets\yellow_front.png"), size=(PLAYER_SIZE, PLAYER_SIZE))
        self.image = self.orig_image.copy()
        self.image_left = image.load(resource_path("Assets\yellow_left.png"), size=(PLAYER_SIZE * SIZE_MULTIPLIER, PLAYER_SIZE * SIZE_MULTIPLIER))
        self.image_left = self.image_left.copy()
        self.image_right = image.load(resource_path("Assets\yellow_right.png"), size=(PLAYER_SIZE * SIZE_MULTIPLIER, PLAYER_SIZE * SIZE_MULTIPLIER))
        self.image_right = self.image_right.copy()
        #self.rect = pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, PLAYER_HITBOX_SIZE[0], PLAYER_HITBOX_SIZE[1])
        self.rect = pygame.Rect(SCREEN_WIDTH//2 - PLAYER_HITBOX_SIZE[0]//2, 
                                SCREEN_HEIGHT//2 - PLAYER_HITBOX_SIZE[1]//2, 
                                PLAYER_HITBOX_SIZE[0], PLAYER_HITBOX_SIZE[1])
        self.left_click = False
        self.right_click = False
        self.pose_tracking = PoseTracking()
        

    def update_image(self):
        if self.pose_tracking.standing:
            self.image = self.orig_image.copy()
            #print("Feet together")
        elif self.pose_tracking.left_leg_up:
            self.image = self.image_left.copy()
            #print("Left leg up")
        elif self.pose_tracking.right_leg_up:
            self.image = self.image_right.copy()
            #print("Right leg up")
        else:
            self.image = self.orig_image.copy()

    def follow_mouse(self): # change the player pos center at the mouse pos
        self.rect.center = pygame.mouse.get_pos()
        #self.pose_tracking.display_pose()

    def follow_mediapipe_pose(self, x, y):
        self.rect.center = (x, y)
        

    def draw_hitbox(self, surface):
        pygame.draw.rect(surface, (200, 60, 0), self.rect)


    def draw(self, surface):
        image.draw(surface, self.image, self.rect.center, pos_mode="center")

        if DRAW_HITBOX:
            self.draw_hitbox(surface)


    def on_object(self, objects): # return a list with all objects that collide with the player hitbox
        return [object for object in objects if self.rect.colliderect(object.rect)]


    def kill_objects(self, objects, score, sounds): # will kill the objects that collide with the player when the left mouse button is pressed
        # Define the ranges for object positions and mouse click conditions
        left_click_range = range(400, 450)
        right_click_range = range(700, 750)

        current_time = time.time()

        #if self.left_click or self.right_click: # if left leg is up or right leg is up       
        #    for object in self.on_object(objects):
        #        object_position = object.rect.topleft[0]

                # Check if the conditions for removing the object are met
        #        if (self.left_click and object_position in left_click_range) or (self.right_click and object_position in right_click_range):
        #            object_score = object.kill(objects)
        #            score += object_score
        #            sounds["popping"].play()
                
        #            print("Bubble popped! {object_position}! +1 point")  # Print message for debugging
                #if object_score < 0: # if object_score > 2 it will play the splash sound
                #    sounds["screaming"].play()
        #else:
        #    self.left_click = False
        #return score
        if self.left_click:
            if not hasattr(self, 'left_leg_up_start'):
                self.left_leg_up_start = current_time
        else:
            self.left_leg_up_start = None
    
        if self.right_click:
            if not hasattr(self, 'right_leg_up_start'):
                self.right_leg_up_start = current_time
        else:
            self.right_leg_up_start = None
        
        for object in self.on_object(objects):
            object_position = object.rect.topleft[0]
        
            #left_leg_up_time = current_time - self.left_leg_up_start if self.left_leg_up_start else 0
            #right_leg_up_time = current_time - self.right_leg_up_start if self.right_leg_up_start else 0
        
            #if ((self.left_click and object_position in left_click_range and left_leg_up_time >= 2) or 
            #    (self.right_click and object_position in right_click_range and right_leg_up_time >= 2)):
            #    print("Leg is up for 2 seconds")
                #if object.can_be_popped(max(left_leg_up_time, right_leg_up_time)):
            object_score = object.kill(objects)
            score += object_score
            sounds["popping"].play()
            print(f"Bubble popped at {object_position}! +{object_score} points")
    
        return score
    

