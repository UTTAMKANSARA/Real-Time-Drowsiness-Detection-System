# To Run Project on the Browser.

# from django.shortcuts import render
# from django.http import StreamingHttpResponse
# from . import detector  # Import your NEW detector logic
# from . import sms_alert   # Import your SMS logic
# import cv2
# import time
# import pygame
# import os
# import mediapipe as mp
# import numpy as np

# # --- Variables for Drowsiness Counter ---
# EYE_FRAME_COUNTER = 0
# YAWN_FRAME_COUNTER = 0 # <--- NEW
# DROWSY_ALARM_ON = False

# # --- Initialize Pygame and load the sound ---
# pygame.mixer.init()
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ALARM_SOUND_PATH = os.path.join(BASE_DIR, 'static', 'alarm.wav')
# try:
#     alarm_sound = pygame.mixer.Sound(ALARM_SOUND_PATH)
# except pygame.error as e:
#     print(f"[WARNING] Could not load alarm sound: {e}")
#     alarm_sound = None

# def video_feed():
#     """Video streaming generator function."""
#     global EYE_FRAME_COUNTER, YAWN_FRAME_COUNTER, DROWSY_ALARM_ON # <--- UPDATED

#     cap = cv2.VideoCapture(0)
#     time.sleep(2.0)

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("Failed to grab frame")
#             break
        
#         (frame_height, frame_width) = frame.shape[:2]

#         # --- MediaPipe Processing ---
#         image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         detector.face_mesh_results = detector.face_mesh.process(image_rgb)
#         image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
#         # --- End MediaPipe Processing ---

#         if detector.face_mesh_results.multi_face_landmarks:
#             # --- Calculate EAR ---
#             ear_left, left_eye_points = detector.calculate_ear(
#                 detector.LEFT_EYE_IDXS, frame_width, frame_height)
#             ear_right, right_eye_points = detector.calculate_ear(
#                 detector.RIGHT_EYE_IDXS, frame_width, frame_height)
#             ear = (ear_left + ear_right) / 2.0

#             # --- Calculate MAR ---
#             mar, mouth_points = detector.calculate_mar(
#                 detector.MOUTH_INNER_IDXS, frame_width, frame_height) # <--- NEW

#             # --- Draw contours ---
#             left_eye_hull = cv2.convexHull(np.array(left_eye_points))
#             right_eye_hull = cv2.convexHull(np.array(right_eye_points))
#             mouth_hull = cv2.convexHull(np.array(mouth_points)) # <--- NEW
            
#             cv2.drawContours(frame, [left_eye_hull], -1, (0, 255, 0), 1)
#             cv2.drawContours(frame, [right_eye_hull], -1, (0, 255, 0), 1)
#             cv2.drawContours(frame, [mouth_hull], -1, (0, 255, 0), 1) # <--- NEW

#             # --- Check for Drowsiness (Eyes) ---
#             if ear < detector.EAR_THRESHOLD:
#                 EYE_FRAME_COUNTER += 1
#             else:
#                 EYE_FRAME_COUNTER = 0

#             # --- Check for Yawning (Mouth) ---
#             if mar > detector.MAR_THRESHOLD: # <--- NEW
#                 YAWN_FRAME_COUNTER += 1
#             else:
#                 YAWN_FRAME_COUNTER = 0
            
#             # --- Trigger Alarm if EITHER condition is met ---
#             if (EYE_FRAME_COUNTER >= detector.EAR_CONSEC_FRAMES) or (YAWN_FRAME_COUNTER >= detector.MAR_CONSEC_FRAMES): # <--- UPDATED
#                 if not DROWSY_ALARM_ON:
#                     DROWSY_ALARM_ON = True
#                     if alarm_sound:
#                         alarm_sound.play(-1)
#                     sms_alert.send_drowsiness_alert()
                
#                 cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
#             else:
#                 # Reset counters and stop alarm
#                 # (Note: We reset eye *and* yawn counters separately now)
#                 if DROWSY_ALARM_ON:
#                     DROWSY_ALARM_ON = False
#                     if alarm_sound:
#                         alarm_sound.stop()
        
#         else:
#             # No face found, reset all
#             EYE_FRAME_COUNTER = 0
#             YAWN_FRAME_COUNTER = 0 # <--- NEW
#             if DROWSY_ALARM_ON:
#                 DROWSY_ALARM_ON = False
#                 if alarm_sound:
#                     alarm_sound.stop()

#         (flag, encodedImage) = cv2.imencode(".jpg", frame)
#         if not flag:
#             continue

#         yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
#                bytearray(encodedImage) + b'\r\n')

#     cap.release()
#     cv2.destroyAllWindows()
#     pygame.mixer.quit()

# def index(request):
#     """Home page view."""
#     return render(request, 'detection/index.html')

# def stream(request):
#     """Video streaming view."""
#     return StreamingHttpResponse(video_feed(), 
#                                  content_type='multipart/x-mixed-replace; boundary=frame')