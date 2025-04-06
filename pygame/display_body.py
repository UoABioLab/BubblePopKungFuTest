import cv2
import numpy as np
import pygame
from mediapipe import solutions as mp_solutions


def Display_Pose(frame, results, screen):
    if results.pose_landmarks:
        # Draw the skeleton on the frame
        mp_solutions.drawing_utils.draw_landmarks(
            frame, results.pose_landmarks, mp_solutions.pose.POSE_CONNECTIONS)

    # Convert the frame to an image that pygame can use
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_rgb = np.rot90(frame_rgb)  # Rotate frame to match Pygame's coordinate system
    frame_surface = pygame.surfarray.make_surface(frame_rgb)

    # 动态调整框的大小，根据屏幕尺寸设置显示框的大小
    frame_width = int(screen.get_width() * 0.25)  # 占屏幕宽度的25%
    frame_height = int(screen.get_height() * 0.25)  # 占屏幕高度的25%
    frame_surface = pygame.transform.scale(frame_surface, (frame_width, frame_height))

    # 将图像显示在屏幕的左下角
    screen.blit(frame_surface, (10, screen.get_height() - frame_height - 10))  # 10px padding from left and bottom