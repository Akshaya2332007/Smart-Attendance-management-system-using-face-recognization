import cv2
import pickle
import sqlite3
from datetime import datetime
from voice import speak

from blink_detector import detect_blink


# ==========================================
# Attendance Function
# ==========================================

def mark_attendance(student_info):

    conn = sqlite3.connect("database/attendance.db")
    cursor = conn.cursor()

    student_id, name = student_info.split("_", 1)

    today = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")

    cursor.execute(
        """
        SELECT *
        FROM attendance
        WHERE student_id=? AND date=?
        """,
        (student_id, today)
    )

    record = cursor.fetchone()

    if record is None:

        cursor.execute(
            """
            INSERT INTO attendance
            (student_id,name,date,time,status)
            VALUES (?,?,?,?,?)
            """,
            (
                student_id,
                name,
                today,
                current_time,
                "Present"
            )
        )

        conn.commit()

        print(f"Attendance marked for {name}")

        return True

    else:

        print(f"Attendance already marked today for {name}")

        return False

    conn.close()


# ==========================================
# Load Face Recognition Model
# ==========================================

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("models/trainer.yml")

with open("models/labels.pkl", "rb") as f:
    labels = pickle.load(f)


# ==========================================
# Haar Cascade
# ==========================================

face_cascade = cv2.CascadeClassifier(

    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"

)


# ==========================================
# Webcam
# ==========================================

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():

    print("Cannot open webcam")
    exit()

attendance_marked = set()
blink_verified = False

print("Face Recognition Started...")
# ==========================================
# Recognition Loop
# ==========================================

while True:

    ret, frame = cap.read()

    if not ret:
        print("Cannot read frame")
        break

    # --------------------------
    # Blink Detection
    # --------------------------

    if not blink_verified:
        blink_verified = detect_blink(frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(100, 100)
    )

    for (x, y, w, h) in faces:

        # If user has not blinked
        if not blink_verified:

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 255),
                2
            )

            cv2.putText(
                frame,
                "Please Blink",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2
            )

            continue

        # --------------------------
        # Face Recognition
        # --------------------------

        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (200, 200))

        label, confidence = recognizer.predict(face)

        display_name = "Unknown"
        color = (0, 0, 255)
        if confidence < 70:

            student_info = labels.get(label, "Unknown")

            if student_info != "Unknown":

                display_name = student_info.split("_", 1)[1]
                color = (0, 255, 0)

                if student_info not in attendance_marked:

                    new_attendance = mark_attendance(student_info)

                    attendance_marked.add(student_info)

                    if new_attendance:
                        speak(
                            f"Welcome {display_name}. Attendance marked successfully."
                        )

                cv2.putText(
                    frame,
                    "FACE RECOGNIZED",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    3
                )

                cv2.putText(
                    frame,
                    f"Student: {display_name}",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    "Attendance Marked",
                    (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 255),
                    2

                )

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            color,
            2
        )

        cv2.putText(
            frame,
            display_name,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

        cv2.putText(
            frame,
            f"Confidence: {int(confidence)}",
            (x, y + h + 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

    cv2.imshow("Smart AI Attendance System", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()