# gesture_control.py
import cv2
import mediapipe as mp
import time  # <-- NEW IMPORT

from gui import update_play_count
from music_controller import pause, play_next, play_previous, is_paused

class GestureController:
    def __init__(self):
        self.cap = cv2.VideoCapture(0) #initialises the webcam capture
        self.mp_hands = mp.solutions.hands #initialises the mediapipe hand soln
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.last_gesture_time = 0  # <-- REPLACED cooldown counter
        self.cooldown = 1.0  # specifies the cooldown period (1 second) between gesture detections

    def count_fingers(self, landmarks): #it compares the y position of the fingertip (tip) and the joint (pip) of each finger to determine whether the finger is up.
        fingers = 0
        # Check fingers (excluding thumb for better reliability)
        for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:  # Index to Pinky
            if landmarks.landmark[tip].y < landmarks.landmark[pip].y: #a finger is extended, the tip moves above the pip, causing the tip's y-coordinate to be lower than the pip's y-coordinate.
                fingers += 1
        return fingers

    def run(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read() #read the frame
            if not ret:
                break

            frame = cv2.flip(frame, 1) # give a mirror effect,
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #converts from BGR TO RGB frame
            results = self.hands.process(rgb_frame) #process the grame with media pipe
            current_time = time.time()  # <-- NEW: Get current time

            if results.multi_hand_landmarks:
                hand = results.multi_hand_landmarks[0] #picks the first detected hand
                fingers = self.count_fingers(hand) #calls count finger method

                # NEW: Time-based cooldown check instead of frame count
                if (current_time - self.last_gesture_time) > self.cooldown:
                    if fingers == 0:  # Fist
                        pause()
                        update_play_count()
                        self.last_gesture_time = current_time
                    elif fingers == 2:  # Two fingers
                        play_next()
                        update_play_count()
                        self.last_gesture_time = current_time
                    elif fingers == 1:  # One finger
                        play_previous()
                        update_play_count()
                        self.last_gesture_time = current_time

                # Draw hand landmarks
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, hand, self.mp_hands.HAND_CONNECTIONS)

            # Display instructions
            cv2.putText(frame, "FIST: Pause/Resume", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "TWO FINGERS: Next", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "ONE FINGER: Previous", (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            cv2.imshow('Gesture Control (ESC to quit)', frame)
            if cv2.waitKey(10) & 0xFF == 27:
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    GestureController().run()