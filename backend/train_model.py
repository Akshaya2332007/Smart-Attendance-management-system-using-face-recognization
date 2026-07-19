import cv2
import os
import numpy as np
import pickle

dataset_path = "dataset"

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

faces = []
labels = []
label_map = {}
current_label = 0

# Read dataset folders
for folder in os.listdir(dataset_path):
    folder_path = os.path.join(dataset_path, folder)

    if not os.path.isdir(folder_path):
        continue

    label_map[current_label] = folder

    for image_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_name)

        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if img is None:
            continue

        # resize (IMPORTANT)
        img = cv2.resize(img, (200, 200))

        faces.append(img)
        labels.append(current_label)

    current_label += 1

faces = np.array(faces)
labels = np.array(labels)

# Train model
recognizer.train(faces, labels)

# Save model
if not os.path.exists("models"):
    os.makedirs("models")

recognizer.save("models/trainer.yml")

# Save labels
with open("models/labels.pkl", "wb") as f:
    pickle.dump(label_map, f)

print("✅ Model trained successfully!")