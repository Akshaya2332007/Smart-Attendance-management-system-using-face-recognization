import cv2
import os

def capture_faces(student_id, student_name):

    # Create dataset folder
    dataset_path = "dataset"
    os.makedirs(dataset_path, exist_ok=True)

    # Create student folder
    student_folder = os.path.join(dataset_path, f"{student_id}_{student_name}")
    os.makedirs(student_folder, exist_ok=True)

    # Create profile photo folder
    os.makedirs("static/photos", exist_ok=True)

    # Face detector
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    cap = cv2.VideoCapture(0)

    count = 0
    max_images = 100

    print(f"📷 Capturing faces for {student_name}...")

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )

        for (x, y, w, h) in faces:

            count += 1

            # Save grayscale image for training
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (200, 200))

            filename = os.path.join(student_folder, f"{count}.jpg")
            cv2.imwrite(filename, face)

            # Save color profile photo
            face_color = frame[y:y+h, x:x+w]
            face_color = cv2.resize(face_color, (200, 200))
            cv2.imwrite(f"static/photos/{student_id}.jpg", face_color)

            # Draw rectangle
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Student name
            cv2.putText(
                frame,
                f"Student: {student_name}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 0, 0),
                2
            )

            # Progress
            cv2.putText(
                frame,
                f"Images: {count}/{max_images}",
                (10, 65),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2
            )

            # Instructions
            cv2.putText(
                frame,
                "Look at the camera",
                (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

        cv2.imshow("Smart AI Face Capture", frame)

        key = cv2.waitKey(1)

        if key == ord("q"):
            break

        if count >= max_images:
            break

    cap.release()
    cv2.destroyAllWindows()

    print(f"✅ {count} images captured for {student_name}")