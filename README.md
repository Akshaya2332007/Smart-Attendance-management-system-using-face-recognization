# 🎓 Smart Attendance Management System using Face Recognition

A Smart Attendance Management System that uses **Face Recognition** and **Blink Detection** to automatically mark student attendance. The system prevents photo spoofing by verifying that the user blinks before attendance is recorded.

---

## 📌 Project Overview

This project automates attendance management by recognizing a student's face through a webcam and verifying liveness using blink detection. Once verified, the student's attendance is stored in the database and can be exported as an Excel report.

---

## ✨ Features

- 👤 Student Registration
- 📷 Face Image Capture
- 🧠 Face Recognition using OpenCV
- 👁️ Blink Detection for Liveness Verification
- ✅ Automatic Attendance Marking
- 🗄️ SQLite Database Integration
- 📊 Attendance Report Generation (Excel)
- 🌐 User-Friendly Flask Web Interface

---

## 🛠️ Technologies Used

- Python
- Flask
- OpenCV
- MediaPipe
- SQLite
- HTML
- CSS
- JavaScript
- OpenPyXL
- NumPy
- Pickle

---

## 📂 Project Structure

```
Smart-Attendance-System/
│
├── backend/
│   ├── face_capture.py
│   ├── recognize_face.py
│   ├── train_model.py
│   ├── blink_detector.py
│   └── voice.py
│
├── database/
│
├── dataset/
│
├── models/
│
├── static/
│
├── templates/
│
├── app.py
├── config.py
├── database.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Clone the Repository

```bash
git clone https://github.com/Akshaya2332007/Smart-Attendance-management-system-using-face-recognization.git
```

### Move into the project

```bash
cd Smart-Attendance-management-system-using-face-recognization
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate the virtual environment

Windows

```bash
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the project

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## 📸 Screenshots

- Login Page
- Student Registration
- Face Recognition
- Attendance Dashboard

*(Add screenshots here later.)*

---

## 📊 Future Enhancements

- Email Attendance Report
- Admin Dashboard
- Cloud Database
- QR Code Attendance
- Mobile Application
- Multi-Face Recognition

---

## 👩‍💻 Author

**Akshaya**

B.Tech Artificial Intelligence & Data Science

GitHub: https://github.com/Akshaya2332007

---

## ⭐ If you like this project

Please give this repository a ⭐ on GitHub.