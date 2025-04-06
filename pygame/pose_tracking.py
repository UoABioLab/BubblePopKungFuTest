import cv2
import mediapipe as mp
from settings import *
import numpy as np
import pandas as pd
import time
import datetime
import os
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose
class PoseTracking:
    def __init__(self):
        #global POSITION_FACTOR
        #self.hand_tracking = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.pose_tracking = mp_pose.Pose(static_image_mode=False, model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.pose_x = 0
        self.pose_y = 0
        self.results = None
        self.arm_up = False
        self.left_leg_up = False
        self.right_leg_up = False
        self.standing = True
        self.all_landmarks = []  # List to store all frames' landmark data
        self.frame_count = 0  # Frame count
    def check_pose(self, image):
        if image is None:
            print("Warning: Received None image in check_pose")
            return np.zeros((480, 640, 3), dtype=np.uint8)
        try:
            # 确保图像是有效的
            if image.size == 0:
                print("Warning: Received empty image in check_pose")
                return np.zeros((480, 640, 3), dtype=np.uint8)
            rows, cols, _ = image.shape
            # 添加图像大小检查
            if rows == 0 or cols == 0:
                print("Warning: Invalid image dimensions")
                return np.zeros((480, 640, 3), dtype=np.uint8)
            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            self.results = self.pose_tracking.process(image)
            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            self.arm_up = False
            self.left_leg_up = False
            self.right_leg_up = False
            self.standing = True
            self.left_timer = 0
            self.right_timer = 0
            self.left_start_time = 0
            self.right_start_time = 0
            if self.results.pose_landmarks:
                # 现有的姿势检测代码...
                landmarks = self.results.pose_landmarks.landmark
                landmark_dict = {
                    'frame': self.frame_count,
                    'timestamp': datetime.datetime.now()
                }
                for lm in mp_pose.PoseLandmark:
                    landmark_dict[f"{lm.name}_x"] = landmarks[lm.value].x
                    landmark_dict[f"{lm.name}_y"] = landmarks[lm.value].y
                self.all_landmarks.append(landmark_dict)
                self.frame_count += 1
                # Draw Pose Landmarks
                mp_drawing.draw_landmarks(
                    image, 
                    self.results.pose_landmarks,
                    connections=mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(
                        color=(255,255,255),
                        thickness=3, 
                        circle_radius=3
                    ),
                    connection_drawing_spec=mp_drawing.DrawingSpec(
                        color=(49,125,237),
                        thickness=2, 
                        circle_radius=2
                    )
                )
            return image
        except Exception as e:
            print(f"Error in check_pose: {e}")
            return np.zeros((480, 640, 3), dtype=np.uint8)
    def save_landmarks_to_csv(self, file_path):
        try:
            df = pd.DataFrame(self.all_landmarks)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            df.to_csv(file_path, index=False)
            print(f"Landmarks from pose_tracking saved to {file_path}")
        except Exception as e:
            print(f"Error saving landmarks to {file_path}: {e}")
    def get_player_center(self):
        return (self.pose_x, self.pose_y)
    def display_pose(self):
        cv2.imshow("image", self.image)
        cv2.waitKey(1)
    def is_arm_up(self):
        pass
