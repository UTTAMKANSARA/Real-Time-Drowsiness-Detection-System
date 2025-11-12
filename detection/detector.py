import mediapipe as mp
import numpy as np
from scipy.spatial import distance as dist
import cv2


FACE_3D_MODEL_POINTS = np.array([
    (0.0, 0.0, 0.0),      
    (0.0, -330.0, -65.0), 
    (-225.0, 170.0, -135.0), 
    (225.0, 170.0, -135.0),  
    (-150.0, -150.0, -125.0), 
    (150.0, -150.0, -125.0)   
], dtype=np.float64)


HEAD_POSE_IDXS = [1, 199, 33, 263, 61, 291]


NOD_THRESHOLD = 15.0  
NOD_CONSEC_FRAMES = 15 



MOUTH_INNER_IDXS = [78, 308, 81, 311, 13, 14, 312, 310] 
MAR_THRESHOLD = 0.7        
MAR_CONSEC_FRAMES = 20       



mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)


LEFT_EYE_IDXS = [362, 385, 387, 263, 373, 380]
RIGHT_EYE_IDXS = [33, 160, 158, 133, 153, 144]


EAR_THRESHOLD = 0.25     
EAR_CONSEC_FRAMES = 15    

def calculate_ear(eye_landmarks, frame_width, frame_height):
    
    
   
    eye_points = []
    for idx in eye_landmarks:
       
        lm = face_mesh_results.multi_face_landmarks[0].landmark[idx]
      
        x = int(lm.x * frame_width)
        y = int(lm.y * frame_height)
        eye_points.append((x, y))

   
    A = dist.euclidean(eye_points[1], eye_points[5])
    B = dist.euclidean(eye_points[2], eye_points[4])
    
   
    C = dist.euclidean(eye_points[0], eye_points[3])
    
    
    ear = (A + B) / (2.0 * C)
    return ear, eye_points


face_mesh_results = None




def calculate_mar(mouth_landmarks, frame_width, frame_height):
    
    mouth_points = []
    for idx in mouth_landmarks:
        lm = face_mesh_results.multi_face_landmarks[0].landmark[idx]
        x = int(lm.x * frame_width)
        y = int(lm.y * frame_height)
        mouth_points.append((x, y))

   
    A = dist.euclidean(mouth_points[1], mouth_points[7])
    B = dist.euclidean(mouth_points[2], mouth_points[6])
    C = dist.euclidean(mouth_points[3], mouth_points[5])
    
   
    D = dist.euclidean(mouth_points[0], mouth_points[4])
    
   
    mar = (A + B + C) / (3.0 * D)
    return mar, mouth_points



def get_head_pose(frame_width, frame_height):
    # """
    # Calculates the head's Pitch, Yaw, and Roll angles.
    # Returns:
    #     pitch (float): Up/Down angle
    #     yaw (float): Left/Right angle
    #     roll (float): Tilted angle
    # """

    
    face_2d_points = []
    for idx in HEAD_POSE_IDXS:
        lm = face_mesh_results.multi_face_landmarks[0].landmark[idx]
        x = int(lm.x * frame_width)
        y = int(lm.y * frame_height)
        face_2d_points.append((x, y))

    face_2d_points = np.array(face_2d_points, dtype=np.float64)

   
    focal_length = frame_width
    cam_center = (frame_width / 2, frame_height / 2)
    camera_matrix = np.array([
        [focal_length, 0, cam_center[0]],
        [0, focal_length, cam_center[1]],
        [0, 0, 1]
    ], dtype=np.float64)

    
    dist_coeffs = np.zeros((4, 1))
    

   
    (success, rvec, tvec) = cv2.solvePnP(
        FACE_3D_MODEL_POINTS, 
        face_2d_points, 
        camera_matrix, 
        dist_coeffs
    )

    
    r_mat, _ = cv2.Rodrigues(rvec)

   
    sy = np.sqrt(r_mat[0, 0] * r_mat[0, 0] + r_mat[1, 0] * r_mat[1, 0])
    singular = sy < 1e-6

    if not singular:
        x = np.arctan2(r_mat[2, 1], r_mat[2, 2])
        y = np.arctan2(-r_mat[2, 0], sy)
        z = np.arctan2(r_mat[1, 0], r_mat[0, 0])
    else:
        x = np.arctan2(-r_mat[1, 2], r_mat[1, 1])
        y = np.arctan2(-r_mat[2, 0], sy)
        z = 0

    
    pitch = np.rad2deg(x)
    yaw = np.rad2deg(y)
    roll = np.rad2deg(z)

    return pitch, yaw, roll