import cv2
import mediapipe as mp
import math

# ---------------------------
# MediaPipe Face Mesh
# ---------------------------
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]


def distance(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)


def eye_ratio(landmarks, eye):
    left = landmarks[eye[0]]
    top1 = landmarks[eye[1]]
    top2 = landmarks[eye[2]]
    right = landmarks[eye[3]]
    bottom1 = landmarks[eye[4]]
    bottom2 = landmarks[eye[5]]

    horizontal = distance(left, right)
    vertical = (distance(top1, bottom1) + distance(top2, bottom2)) / 2

    return vertical / horizontal


# ---------------------------
# Blink Variables
# ---------------------------
blink_counter = 0
blink_detected = False

# Adjust this value if needed
BLINK_THRESHOLD = 0.45


def detect_blink(frame):
    global blink_counter
    global blink_detected

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if not results.multi_face_landmarks:
        return False

    landmarks = results.multi_face_landmarks[0].landmark

    left_ratio = eye_ratio(landmarks, LEFT_EYE)
    right_ratio = eye_ratio(landmarks, RIGHT_EYE)

    ear = (left_ratio + right_ratio) / 2

    print("EAR:", round(ear, 3))

    # Eyes closed
    if ear < BLINK_THRESHOLD:
        blink_counter += 1

    # Eyes opened again
    else:
        if blink_counter >= 2:
            blink_detected = True

        blink_counter = 0

    if blink_detected:
        blink_detected = False
        return True

    return False