import pygame
import time
import random
from settings import *
from settings import settings, update_difficulty_settings
from background import Background
from player import Player
from pose_tracking import PoseTracking
from bubble import Bubble
from balloon import Balloon
import cv2
import numpy as np
import UI
import os
import datetime
from difficulty import Difficulty
from pygame import gfxdraw
from upload_to_goolge_sheets import upload_to_google_sheets
from relative_path import resource_path
from countdown import CountdownScreen
class Game:
    def __init__(self, surface, USER_ID=None, LEVEL=None): 
        self.surface = surface
        self.background = Background()
        self.lives = LIVES
        # 初始化 pose_tracking 和 player
        self.pose_tracking = PoseTracking()
        self.player = Player()
        # For countdown
        self.countdown_screen = None
        self.game_started = False
        # Added from Star Catcher
        self.user_id = USER_ID
        self.level = LEVEL
        print(f"Game: Initialized with USER_ID = {USER_ID}, LEVEL = {LEVEL}")
        # Initialize difficulty setting
        if LEVEL is not None:
            print("Difficulty level passed to GAME")
            self.difficulty = Difficulty(surface, SCREEN_WIDTH, SCREEN_HEIGHT)
            self.difficulty_settings = self.difficulty.difficulties[LEVEL]
            self.apply_difficulty_settings(self.difficulty_settings)
        else:
            print("Warning: Game initialized without a difficulty level")
        # Load camera with retry mechanism
        self.cap = None
        self.initialize_camera()
        # List the sounds
        self.sounds = {}
        self.sounds["popping"] = pygame.mixer.Sound(resource_path("Assets/pop_sound.mp3"))
        self.sounds["popping"].set_volume(SOUNDS_VOLUME)
        self.sounds["screaming"] = pygame.mixer.Sound(resource_path("Assets/splash.wav"))
        self.sounds["screaming"].set_volume(SOUNDS_VOLUME)
        # 初始化其他属性
        self.difficulty_level = "Normal"  
        self.landmark_file_path = None
        self.all_landmarks = []  
        self.game_over = False
        self.left_leg_up_start = None
        self.right_leg_up_start = None
        self.countdown_font = pygame.font.Font(None, 60)
        # 游戏启动倒计时
        self.game_countdown_time = 5  
        self.game_started = False  
        self.game_countdown_start_time = None  
        self.game_countdown_font = pygame.font.Font(None, 60)  
        # 初始化游戏对象列表和计时器
        self.objects = []
        self.objects_spawn_timer = 0
        self.score = 0
        self.game_start_time = time.time()
    def initialize_camera(self):
        """Initialize the camera with retry mechanism"""
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                if self.cap is not None:
                    self.cap.release()
                self.cap = cv2.VideoCapture(0)
                if self.cap.isOpened():
                    ret, test_frame = self.cap.read()
                    if ret and test_frame is not None:
                        print("Camera initialized successfully")
                        return
            except Exception as e:
                print(f"Camera initialization attempt {attempt + 1} failed: {e}")
            time.sleep(1)  # Wait before retry
        print("Warning: Could not initialize camera after multiple attempts")
    def start_game_countdown(self):
       """初始化游戏倒计时"""
       self.game_countdown_start_time = time.time()  # 记录倒计时开始的时间
    def draw_game_countdown(self, seconds_left):
       #"""在屏幕上绘制游戏启动倒计时"""
        # Fill the background with black color
        self.background.draw(self.surface)
        timer_pos = (600, 200)
        radius = 50
        color = (255, 0, 0)  # 红色圆圈
        gfxdraw.aacircle(self.surface, timer_pos[0], timer_pos[1], radius, color)
        gfxdraw.filled_circle(self.surface, timer_pos[0], timer_pos[1], radius, color)
        # 绘制倒计时数字
        text = self.countdown_font.render(f"{seconds_left:.1f}", True, (255, 255, 255))
        text_rect = text.get_rect(center=timer_pos)
        self.surface.blit(text, text_rect)
        # Capture frame from camera and perform pose tracking
        self.load_camera()  # Load camera frame
        self.set_player_position()  # Update player position based on pose tracking
       # Display the video frame in the corner
        self.show_frame_in_pygame()
    # def start_countdown(self):
    #     """Initialize the countdown screen and start it."""
    #     self.countdown_screen = CountdownScreen(self.surface, countdown_time=5, cap=self.cap)
    #     self.countdown_screen.start()
    def reset(self): # reset all the needed variables
        print("Entering game reset")
        if self.difficulty_settings:
            self.apply_difficulty_settings(self.difficulty_settings)
            self.pose_tracking = PoseTracking()
            self.player = Player()
            self.player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.objects = []
            #self.objects_spawn_timer = time.time()  # Initialize the spawn timer
            self.objects_spawn_timer = 0
            self.score = 0
            #self.lives = LIVES
            self.game_start_time = time.time()
            self.balloon_pos = []
            self.bubble_pos = []
            self.game_over = False
            self.all_landmarks = []  # List to store all frames' landmark data
            # Set up the landmark file path
            current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bubble_pop_{self.user_id}_{self.level}_{current_time}.csv"
            self.landmark_file_path = os.path.join("Position_data", filename)
        print("Exiting game reset")    
    def apply_difficulty_settings(self, difficulty_settings):
        try:
            self.difficulty_settings = difficulty_settings
            print(f"Game: Applying difficulty settings: {self.difficulty_settings}")
    #        self.difficulty_level = self.difficulty_manager.difficulty  # Assume this exists in your settings
            # Check if difficulty_settings is a dictionary
            if isinstance(difficulty_settings, dict):
                # Access dictionary keys
                update_difficulty_settings(
                    difficulty_settings['SPAWN_TIME'],
                    difficulty_settings['VELOCITY'],
                    difficulty_settings['LEG_UP_TIME']
                )
            else:
                # Access as object attributes
                update_difficulty_settings(
                    difficulty_settings.SPAWN_TIME,
                    difficulty_settings.VELOCITY,
                    difficulty_settings.LEG_UP_TIME
                )
            print(f"Game: After Update LEG UP TIME: {settings.LEG_UP_TIME}")
        except Exception as e:
            print(f"Error applying difficulty settings: {e}")
            raise
    def spawn_objects(self):
        if LIVES > 0:
            t = time.time()
            if t > self.objects_spawn_timer:
                self.objects_spawn_timer = t + settings.SPAWN_TIME
                # Add difficulty settings to spawned object
                new_object = Bubble(velocity=settings.VELOCITY)
                self.objects.append(new_object)
                print(f"Spawned a balloon with velocity: {settings.VELOCITY}")
                # Code to randomly spawn bubble or balloon
                #balloon_probability = (GAME_DURATION - self.time_left) / GAME_DURATION * 50  # Increases from 0 to 50% during the game
                #print(f"Spawning object. Balloon probability: {balloon_probability}")
                #if random.random() * 100 < balloon_probability: #uaw this or the next line
                #if balloon_probability > 40:
                #    new_object = Balloon()
                    #self.objects.append(Balloon())
                #else:
                #    new_object = Bubble(velocity=self.bubble_move_speed)
                    #self.objects.append(Bubble())
                #    print("Spawned a Bubble")
                #    self.objects.append(new_object) # Add spawned object to list
    def load_camera(self):
        _, self.frame = self.cap.read()
    def set_player_position(self):
        self.frame = self.pose_tracking.check_pose(self.frame)
        (x, y) = self.pose_tracking.get_player_center()
        self.player.rect.center = (x, y)
    def draw(self):
        # draw the background
        self.background.draw(self.surface)
        # draw the objects
        for object in self.objects:
            object.draw(self.surface)
        # draw the player
        self.player.draw(self.surface)
        # draw the score
        UI.draw_text(self.surface, f"Score : {self.score}", (10, 5), COLORS["score"], font=FONTS["medium"],
                    shadow=True, shadow_color=(255,255,255))
        # draw the number of lives
        UI.draw_text(self.surface, f"Lives : {LIVES}", (450, 5), COLORS["score"], font=FONTS["medium"],
                    shadow=True, shadow_color=(255,255,255))
        # draw the time left
        timer_text_color = (160, 40, 0) if self.time_left < 5 else COLORS["timer"] # change the text color if less than 5 s left
        UI.draw_text(self.surface, f"Time left : {self.time_left}", (850, 5),  timer_text_color, font=FONTS["medium"],
                    shadow=True, shadow_color=(255,255,255))
import pygame
import time
import random
from settings import *
from settings import settings, update_difficulty_settings
from background import Background
from player import Player
from pose_tracking import PoseTracking
from bubble import Bubble
from balloon import Balloon
import cv2
import numpy as np
import UI
import os
import datetime
from difficulty import Difficulty
from pygame import gfxdraw
from upload_to_goolge_sheets import upload_to_google_sheets
from relative_path import resource_path
from countdown import CountdownScreen
class Game:
    def __init__(self, surface, USER_ID=None, LEVEL=None): 
        self.surface = surface
        self.background = Background()
        self.lives = LIVES
        # 初始化 pose_tracking 和 player
        self.pose_tracking = PoseTracking()
        self.player = Player()
        # For countdown
        self.countdown_screen = None
        self.game_started = False
        # Added from Star Catcher
        self.user_id = USER_ID
        self.level = LEVEL
        print(f"Game: Initialized with USER_ID = {USER_ID}, LEVEL = {LEVEL}")
        # Initialize difficulty setting
        if LEVEL is not None:
            print("Difficulty level passed to GAME")
            self.difficulty = Difficulty(surface, SCREEN_WIDTH, SCREEN_HEIGHT)
            self.difficulty_settings = self.difficulty.difficulties[LEVEL]
            self.apply_difficulty_settings(self.difficulty_settings)
        else:
            print("Warning: Game initialized without a difficulty level")
        # Load camera with retry mechanism
        self.cap = None
        self.initialize_camera()
        # List the sounds
        self.sounds = {}
        self.sounds["popping"] = pygame.mixer.Sound(resource_path("Assets/pop_sound.mp3"))
        self.sounds["popping"].set_volume(SOUNDS_VOLUME)
        self.sounds["screaming"] = pygame.mixer.Sound(resource_path("Assets/splash.wav"))
        self.sounds["screaming"].set_volume(SOUNDS_VOLUME)
        # 初始化其他属性
        self.difficulty_level = "Normal"  
        self.landmark_file_path = None
        self.all_landmarks = []  
        self.game_over = False
        self.left_leg_up_start = None
        self.right_leg_up_start = None
        self.countdown_font = pygame.font.Font(None, 60)
        # 游戏启动倒计时
        self.game_countdown_time = 5  
        self.game_started = False  
        self.game_countdown_start_time = None  
        self.game_countdown_font = pygame.font.Font(None, 60)  
        # 初始化游戏对象列表和计时器
        self.objects = []
        self.objects_spawn_timer = 0
        self.score = 0
        self.game_start_time = time.time()
    def initialize_camera(self):
        """Initialize the camera with retry mechanism"""
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                if self.cap is not None:
                    self.cap.release()
                self.cap = cv2.VideoCapture(0)
                if self.cap.isOpened():
                    ret, test_frame = self.cap.read()
                    if ret and test_frame is not None:
                        print("Camera initialized successfully")
                        return
            except Exception as e:
                print(f"Camera initialization attempt {attempt + 1} failed: {e}")
            time.sleep(1)  # Wait before retry
        print("Warning: Could not initialize camera after multiple attempts")
    def start_game_countdown(self):
       """初始化游戏倒计时"""
       self.game_countdown_start_time = time.time()  # 记录倒计时开始的时间
    def draw_game_countdown(self, seconds_left):
       #"""在屏幕上绘制游戏启动倒计时"""
        # Fill the background with black color
        self.background.draw(self.surface)
        timer_pos = (600, 200)
        radius = 50
        color = (255, 0, 0)  # 红色圆圈
        gfxdraw.aacircle(self.surface, timer_pos[0], timer_pos[1], radius, color)
        gfxdraw.filled_circle(self.surface, timer_pos[0], timer_pos[1], radius, color)
        # 绘制倒计时数字
        text = self.countdown_font.render(f"{seconds_left:.1f}", True, (255, 255, 255))
        text_rect = text.get_rect(center=timer_pos)
        self.surface.blit(text, text_rect)
        # Capture frame from camera and perform pose tracking
        self.load_camera()  # Load camera frame
        self.set_player_position()  # Update player position based on pose tracking
       # Display the video frame in the corner
        self.show_frame_in_pygame()
    # def start_countdown(self):
    #     """Initialize the countdown screen and start it."""
    #     self.countdown_screen = CountdownScreen(self.surface, countdown_time=5, cap=self.cap)
    #     self.countdown_screen.start()
    def reset(self): # reset all the needed variables
        print("Entering game reset")
        if self.difficulty_settings:
            self.apply_difficulty_settings(self.difficulty_settings)
            self.pose_tracking = PoseTracking()
            self.player = Player()
            self.player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.objects = []
            #self.objects_spawn_timer = time.time()  # Initialize the spawn timer
            self.objects_spawn_timer = 0
            self.score = 0
            #self.lives = LIVES
            self.game_start_time = time.time()
            self.balloon_pos = []
            self.bubble_pos = []
            self.game_over = False
            self.all_landmarks = []  # List to store all frames' landmark data
            # Set up the landmark file path
            current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bubble_pop_{self.user_id}_{self.level}_{current_time}.csv"
            self.landmark_file_path = os.path.join("Position_data", filename)
        print("Exiting game reset")    
    def apply_difficulty_settings(self, difficulty_settings):
        try:
            self.difficulty_settings = difficulty_settings
            print(f"Game: Applying difficulty settings: {self.difficulty_settings}")
    #        self.difficulty_level = self.difficulty_manager.difficulty  # Assume this exists in your settings
            # Check if difficulty_settings is a dictionary
            if isinstance(difficulty_settings, dict):
                # Access dictionary keys
                update_difficulty_settings(
                    difficulty_settings['SPAWN_TIME'],
                    difficulty_settings['VELOCITY'],
                    difficulty_settings['LEG_UP_TIME']
                )
            else:
                # Access as object attributes
                update_difficulty_settings(
                    difficulty_settings.SPAWN_TIME,
                    difficulty_settings.VELOCITY,
                    difficulty_settings.LEG_UP_TIME
                )
            print(f"Game: After Update LEG UP TIME: {settings.LEG_UP_TIME}")
        except Exception as e:
            print(f"Error applying difficulty settings: {e}")
            raise
    def spawn_objects(self):
        if LIVES > 0:
            t = time.time()
            if t > self.objects_spawn_timer:
                self.objects_spawn_timer = t + settings.SPAWN_TIME
                # Add difficulty settings to spawned object
                new_object = Bubble(velocity=settings.VELOCITY)
                self.objects.append(new_object)
                print(f"Spawned a balloon with velocity: {settings.VELOCITY}")
                # Code to randomly spawn bubble or balloon
                #balloon_probability = (GAME_DURATION - self.time_left) / GAME_DURATION * 50  # Increases from 0 to 50% during the game
                #print(f"Spawning object. Balloon probability: {balloon_probability}")
                #if random.random() * 100 < balloon_probability: #uaw this or the next line
                #if balloon_probability > 40:
                #    new_object = Balloon()
                    #self.objects.append(Balloon())
                #else:
                #    new_object = Bubble(velocity=self.bubble_move_speed)
                    #self.objects.append(Bubble())
                #    print("Spawned a Bubble")
                #    self.objects.append(new_object) # Add spawned object to list
    def load_camera(self):
        _, self.frame = self.cap.read()
    def set_player_position(self):
        self.frame = self.pose_tracking.check_pose(self.frame)
        (x, y) = self.pose_tracking.get_player_center()
        self.player.rect.center = (x, y)
    def draw(self):
        # draw the background
        self.background.draw(self.surface)
        # draw the objects
        for object in self.objects:
            object.draw(self.surface)
        # draw the player
        self.player.draw(self.surface)
        # draw the score
        UI.draw_text(self.surface, f"Score : {self.score}", (10, 5), COLORS["score"], font=FONTS["medium"],
                    shadow=True, shadow_color=(255,255,255))
        # draw the number of lives
        UI.draw_text(self.surface, f"Lives : {LIVES}", (450, 5), COLORS["score"], font=FONTS["medium"],
                    shadow=True, shadow_color=(255,255,255))
        # draw the time left
        timer_text_color = (160, 40, 0) if self.time_left < 5 else COLORS["timer"] # change the text color if less than 5 s left
        UI.draw_text(self.surface, f"Time left : {self.time_left}", (850, 5),  timer_text_color, font=FONTS["medium"],
                    shadow=True, shadow_color=(255,255,255))
        # Display the OpenCV frame in the bottom-left corner of the game screen
        self.show_frame_in_pygame()
    def game_time_update(self):
        if LIVES > 0:
            self.time_left = max(round(GAME_DURATION - (time.time() - self.game_start_time), 1), 0)
    def save_landmarks_data(self):
        if self.landmark_file_path and hasattr(self, 'pose_tracking'):
            self.pose_tracking.save_landmarks_to_csv(self.landmark_file_path)
            print(f"Landmarks saved to {self.landmark_file_path}")
    def draw_countdown_timer(self, seconds_left):
        timer_pos = (600, 200)
        radius = 50
        color = (255, 0, 0)  # Red color
        # Draw circle
        gfxdraw.aacircle(self.surface, timer_pos[0], timer_pos[1], radius, color)
        gfxdraw.filled_circle(self.surface, timer_pos[0], timer_pos[1], radius, color)
        # Draw text
        text = self.countdown_font.render(f"{seconds_left:.1f}", True, (255, 255, 255))
        text_rect = text.get_rect(center=timer_pos)
        self.surface.blit(text, text_rect)
    def display_game_over(self):
        game_over_font = pygame.font.Font(None, 100)  # 选择字体和大小
        game_over_text = game_over_font.render("Game Over", True, (0, 0, 0))  # 渲染“Game Over”文本，红色
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))  # 将文本居中
        self.surface.blit(game_over_text, text_rect)  # 将文本绘制到屏幕上
    def reset_game_from_countdown(self):
        #"""Reset the game and start the countdown again."""
        global LIVES
        print("Restarting game from countdown...")
        # Reset the number of lives
        LIVES = 3
        # Reset the game state to initiate countdown again
        self.game_started = False
        self.game_countdown_start_time = None  # Reset countdown timer
        # Reset game variables (score, objects, etc.)
        self.reset()
        # Restart the countdown
        self.start_game_countdown()
    def show_frame_in_pygame(self):
        # Ensure the frame is available
        if self.frame is not None:
            # Get the original dimensions of the frame
            original_height, original_width = self.frame.shape[:2]
            # Calculate new dimensions (1/4 of the original size)
            new_width = original_width // 2
            new_height = original_height // 2
            # Resize the frame
            frame_resized = cv2.resize(self.frame, (new_width, new_height))
            # Convert the OpenCV frame (BGR) to RGB (pygame uses RGB)
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            # Convert the frame to a pygame surface
            frame_surface = pygame.surfarray.make_surface(np.transpose(frame_rgb, (1, 0, 2)))
            # Blit the frame onto the pygame surface at the bottom-left corner
            self.surface.blit(frame_surface, (0, SCREEN_HEIGHT - new_height))
    def update(self):
        global LIVES
        #Step 1: 如果游戏还没有开始，先进行 game countdown
        if not self.game_started:
            if self.game_countdown_start_time is None:
                self.start_game_countdown()  # 初始化倒计时
            # 算倒计时剩余时间
            elapsed_time = time.time() - self.game_countdown_start_time
            game_seconds_left = max(0, self.game_countdown_time - int(elapsed_time))
            # 绘制游戏启动倒计时
            self.draw_game_countdown(game_seconds_left)
            # 倒计时结束，标记游戏正式开始
            if game_seconds_left <= 0:
                self.game_started = True
        # if self.countdown_screen and not self.game_started:
        #     countdown_finished = self.countdown_screen.update()
        #
        #     # If countdown is finished, start the game
        #     if countdown_finished:
        #         self.game_started = True
        #         self.countdown_screen = None  # Clear the countdown screen once it's done
        #
        # elif self.game_started:
        #     self.load_camera()
        #     self.set_player_position()
        #     self.game_time_update()
        #     self.draw()
        # Step 2: 倒计时结束后，游戏开始，执行正常的更新逻辑
        if self.game_started:
            self.load_camera()
            self.set_player_position()
            self.game_time_update()
            self.draw()
