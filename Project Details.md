# Smart Attendance Management System Using Face Recognition

## Project Title

**Smart Attendance Management System Using Face Recognition**

## Problem Statement

Traditional attendance systems are time-consuming, prone to human errors, and vulnerable to proxy attendance. Educational institutions require an automated, secure, and efficient attendance management solution. This project uses face recognition technology to identify students and mark attendance automatically, reducing manual effort and improving accuracy.

## Project Objectives

1. To automate the attendance marking process using facial recognition.
2. To eliminate proxy attendance and improve authenticity.
3. To reduce the time required for attendance management.
4. To maintain accurate attendance records in a database.
5. To generate attendance reports for monitoring and analysis.
6. To provide a user-friendly interface for administrators and faculty.

## Module List

1. User Authentication Module
2. Student Registration Module
3. Face Dataset Collection Module
4. Face Recognition Module
5. Attendance Management Module
6. Database Management Module
7. Report Generation Module

## Table List (Database Tables)

### 1. Students

| Field Name | Data Type |
| ---------- | --------- |
| Student_ID | INT       |
| Name       | VARCHAR   |
| Department | VARCHAR   |
| Year       | INT       |
| Face_ID    | VARCHAR   |

### 2. Attendance

| Field Name    | Data Type |
| ------------- | --------- |
| Attendance_ID | INT       |
| Student_ID    | INT       |
| Date          | DATE      |
| Time          | TIME      |
| Status        | VARCHAR   |

### 3. Users

| Field Name | Data Type |
| ---------- | --------- |
| User_ID    | INT       |
| Username   | VARCHAR   |
| Password   | VARCHAR   |
| Role       | VARCHAR   |

### 4. Face_Data

| Field Name | Data Type |
| ---------- | --------- |
| Face_ID    | VARCHAR   |
| Student_ID | INT       |
| Image_Path | VARCHAR   |

## Expected Outcome

The system will automatically recognize registered students and mark their attendance accurately, reducing manual work and improving attendance management efficiency.
