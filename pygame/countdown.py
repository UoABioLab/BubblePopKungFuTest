import cv2
import pygame
import time
import numpy as np

class CountdownScreen:
    def __init__(self, surface, countdown_time, cap, screen_height):
        """
        Initialize the CountdownScreen.
        :param surface: The pygame surface where the countdown and frame will be shown.
        :param countdown_time: The total time for the countdown (in seconds).
        :param cap: The OpenCV VideoCapture object for displaying the camera feed.
        """
        self.surface = surface
        self.countdown_time = countdown_time
        self.cap = cap
        self.start_time = None
        self.countdown_font = pygame.font.Font(None, 60)  # Font for displaying countdown numbers
        self.frame = None
        self.screen_height = screen_height  # Store the screen height


    def start(self):
        """Start the countdown timer."""
        self.start_time = time.time()

    def update(self):
        """Update the countdown and display the frame."""
        # Calculate remaining time
        elapsed_time = time.time() - self.start_time
        seconds_left = max(0, self.countdown_time - int(elapsed_time))

        # Draw countdown timer on screen
        self.draw_countdown_timer(seconds_left)

        # Show the camera frame on screen
        self.show_frame()

        # Return True when countdown is over
        return seconds_left == 0


    def draw_countdown_timer(self, seconds_left):
        """Draws the countdown timer on the screen."""
        timer_pos = (600, 200)
        radius = 50
        color = (255, 0, 0)  # Red color for the circle

        # Draw the countdown circle
        pygame.gfxdraw.aacircle(self.surface, timer_pos[0], timer_pos[1], radius, color)
        pygame.gfxdraw.filled_circle(self.surface, timer_pos[0], timer_pos[1], radius, color)

        # Draw the countdown number
        text = self.countdown_font.render(f"{seconds_left:.1f}", True, (255, 255, 255))
        text_rect = text.get_rect(center=timer_pos)
        self.surface.blit(text, text_rect)

    def show_frame(self):
        """Display the camera frame resized to 1/4 of the original size in the bottom-left corner."""
        _, self.frame = self.cap.read()  # Capture a frame from the camera

        # Check if the frame is available
        if self.frame is not None:
            # Get original dimensions of the frame
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
            self.surface.blit(frame_surface, (0, self.screen_height - new_height))