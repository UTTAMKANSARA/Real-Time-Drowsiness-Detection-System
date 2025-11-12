
import tkinter as tk
from tkinter import font
import cv2
import pygame
import os
import time
import numpy as np
from PIL import Image, ImageTk


from detection import detector
from detection import sms_alert
pygame.mixer.init()

EYE_FRAME_COUNTER = 0
YAWN_FRAME_COUNTER = 0
HEAD_NOD_COUNTER = 0
DROWSY_ALARM_ON = False


BLINK_TIMESTAMPS = [] 
EYE_STATE = "OPEN"
FRAMES_CLOSED = 0
FRAMES_OPEN = 0


class DrowsyDetectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drowsiness Detection System")
        self.root.geometry("800x700")

        
        self.video_label = tk.Label(root)
        self.video_label.pack(pady=10)

        
        self.status_font = font.Font(family="Helvetica", size=20, weight="bold")
        self.status_label = tk.Label(root, text="STATUS: AWAKE", font=self.status_font, fg="green")
        self.status_label.pack(pady=10)

    
        self.blink_font = font.Font(family="Helvetica", size=16)
        self.blink_label = tk.Label(root, text="Blink Rate: -- BPM", font=self.blink_font, fg="blue")
        self.blink_label.pack(pady=5)
        
        
        self.head_pose_label = tk.Label(root, text="Head Pitch: --°", font=self.blink_font, fg="#555")
        self.head_pose_label.pack(pady=5)


        
        try:
            self.alarm_sound = pygame.mixer.Sound("static/alarm.wav")
        except pygame.error as e:
            print(f"[WARNING] Could not load alarm sound: {e}")
            self.alarm_sound = None

        
        self.cap = cv2.VideoCapture(0)
        time.sleep(2.0) 

        
        self.video_loop()

    def video_loop(self):
        """Main loop to capture video, process it, and update the GUI."""
        global EYE_FRAME_COUNTER, YAWN_FRAME_COUNTER, HEAD_NOD_COUNTER, DROWSY_ALARM_ON
        global BLINK_TIMESTAMPS, EYE_STATE, FRAMES_CLOSED, FRAMES_OPEN 

        ret, frame = self.cap.read()
        if not ret:
            print("Failed to grab frame")
            self.root.after(10, self.video_loop) 
            return

        (frame_height, frame_width) = frame.shape[:2]

        
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detector.face_mesh_results = detector.face_mesh.process(image_rgb)
        display_frame = frame.copy() 
        

        alert_triggered = False 
        BLINK_RATE = 0 
        pitch = 0 

        if detector.face_mesh_results.multi_face_landmarks:
            
            ear_left, left_eye_points = detector.calculate_ear(
                detector.LEFT_EYE_IDXS, frame_width, frame_height)
            ear_right, right_eye_points = detector.calculate_ear(
                detector.RIGHT_EYE_IDXS, frame_width, frame_height)
            ear = (ear_left + ear_right) / 2.0

            
            mar, mouth_points = detector.calculate_mar(
                detector.MOUTH_INNER_IDXS, frame_width, frame_height)
                
        
            pitch, yaw, roll = detector.get_head_pose(frame_width, frame_height)
            
            
            
            if ear < detector.EAR_THRESHOLD:
                FRAMES_OPEN = 0
                FRAMES_CLOSED += 1
                if EYE_STATE == "OPEN" and FRAMES_CLOSED > 2: 
                    EYE_STATE = "CLOSED"
            else:
                FRAMES_CLOSED = 0
                FRAMES_OPEN += 1
                if EYE_STATE == "CLOSED" and FRAMES_OPEN > 2:
                    EYE_STATE = "OPEN"
                    BLINK_TIMESTAMPS.append(time.time())
            
            
            current_time = time.time()
            valid_blinks = [t for t in BLINK_TIMESTAMPS if t > (current_time - 60)]
            BLINK_TIMESTAMPS = valid_blinks 
            BLINK_RATE = len(BLINK_TIMESTAMPS)
            
            
            left_eye_hull = cv2.convexHull(np.array(left_eye_points))
            right_eye_hull = cv2.convexHull(np.array(right_eye_points))
            mouth_hull = cv2.convexHull(np.array(mouth_points))
            
            cv2.drawContours(display_frame, [left_eye_hull], -1, (0, 255, 0), 1)
            cv2.drawContours(display_frame, [right_eye_hull], -1, (0, 255, 0), 1)
            cv2.drawContours(display_frame, [mouth_hull], -1, (0, 255, 0), 1)

            
            if ear < detector.EAR_THRESHOLD:
                EYE_FRAME_COUNTER += 1
            else:
                EYE_FRAME_COUNTER = 0

            
            if mar > detector.MAR_THRESHOLD:
                YAWN_FRAME_COUNTER += 1
            else:
                YAWN_FRAME_COUNTER = 0
                
            
            if pitch > detector.NOD_THRESHOLD:
                HEAD_NOD_COUNTER += 1
            else:
                HEAD_NOD_COUNTER = 0
            
            
            
            if (EYE_FRAME_COUNTER >= detector.EAR_CONSEC_FRAMES) or \
               (YAWN_FRAME_COUNTER >= detector.MAR_CONSEC_FRAMES) or \
               (HEAD_NOD_COUNTER >= detector.NOD_CONSEC_FRAMES):
                
                alert_triggered = True
                if not DROWSY_ALARM_ON:
                    DROWSY_ALARM_ON = True
                    if self.alarm_sound:
                        self.alarm_sound.play(-1)
                    sms_alert.send_drowsiness_alert()
                
                cv2.putText(display_frame, "DROWSINESS ALERT!", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            else:
                if DROWSY_ALARM_ON:
                    DROWSY_ALARM_ON = False
                    if self.alarm_sound:
                        self.alarm_sound.stop()
            
        else:
            
            EYE_FRAME_COUNTER = 0
            YAWN_FRAME_COUNTER = 0
            HEAD_NOD_COUNTER = 0 
            EYE_STATE = "OPEN"
            if DROWSY_ALARM_ON:
                DROWSY_ALARM_ON = False
                if self.alarm_sound:
                    self.alarm_sound.stop()

        
        if alert_triggered:
            self.status_label.config(text="STATUS: DROWSY", fg="red")
        else:
            self.status_label.config(text="STATUS: AWAKE", fg="green")
            
        
        self.blink_label.config(text=f"Blink Rate: {BLINK_RATE} BPM") 
        
        
        self.head_pose_label.config(text=f"Head Pitch: {pitch:.0f}°")
        

        
        img_rgb = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB) 
        img_pil = Image.fromarray(img_rgb) 
        img_tk = ImageTk.PhotoImage(image=img_pil) 
        
        self.video_label.imgtk = img_tk
        self.video_label.configure(image=img_tk)

        
        self.root.after(10, self.video_loop)

    def on_closing(self):
        """Called when the window is closed."""
        print("[INFO] Stopping...")
        self.cap.release()
        pygame.mixer.quit()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = DrowsyDetectApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()