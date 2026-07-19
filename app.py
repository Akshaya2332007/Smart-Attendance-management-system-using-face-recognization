from flask import Flask, render_template, request, redirect, url_for,send_file,session
import sqlite3
import subprocess
import sys
from datetime import datetime
from openpyxl import Workbook



from backend.face_capture import capture_faces
from email_report import send_report

app = Flask(__name__)
app.secret_key = "smart_ai_attendance_2026"

DATABASE = "database/attendance.db"

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "jk" and password == "2211006":

            session["logged_in"] = True

            return redirect(url_for("home"))

        return render_template(
            "login.html",
            error="Invalid Username or Password"
        )

    return render_template("login.html")
# ---------------- HOME ----------------
@app.route("/")
def home():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Total students
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    # Today's attendance
    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute(
        "SELECT COUNT(*) FROM attendance WHERE date=?",
        (today,)
    )
    today_attendance = cursor.fetchone()[0]

    # Today's absent students
    absent_today = total_students - today_attendance

    # Attendance percentage
    if total_students > 0:
        attendance_percentage = round(
            (today_attendance / total_students) * 100,
            2
        )
    else:
        attendance_percentage = 0

    # Total attendance
    cursor.execute("SELECT COUNT(*) FROM attendance")
    total_attendance = cursor.fetchone()[0]
    cursor.execute("""
    SELECT student_id, name, date, time
    FROM attendance
    ORDER BY date DESC, time DESC
    LIMIT 1
""")

    last_student = cursor.fetchone()
    # Recent Attendance (Last 5 Records)
    cursor.execute("""
        SELECT name, date, time
        FROM attendance
        ORDER BY date DESC, time DESC
        LIMIT 5
    """)
    recent_attendance = cursor.fetchall()

    conn.close()

    return render_template(
    "index.html",
    total_students=total_students,
    today_attendance=today_attendance,
    total_attendance=total_attendance,
    absent_today=absent_today,
    attendance_percentage=attendance_percentage,
    recent_attendance=recent_attendance,
    last_student=last_student
)

# ---------------- REGISTER STUDENT ----------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        student_id = request.form["student_id"]
        name = request.form["name"]
        department = request.form["department"]
        year = request.form["year"]
        email = request.form["email"]
        phone = request.form["phone"]

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO students
            (student_id, name, department, year, email, phone)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            student_id,
            name,
            department,
            year,
            email,
            phone
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("students"))

    return render_template("register.html")


# ---------------- VIEW STUDENTS ----------------
@app.route("/students")
def students():

    search = request.args.get("search", "")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if search:
        cursor.execute("""
            SELECT student_id, name, department, year, email, phone
            FROM students
            WHERE student_id LIKE ? OR name LIKE ?
        """, (f"%{search}%", f"%{search}%"))
    else:
        cursor.execute("""
            SELECT student_id, name, department, year, email, phone
            FROM students
        """)

    students = cursor.fetchall()
    conn.close()

    return render_template(
        "students.html",
        students=students,
        search=search
    )

# ---------------- EDIT STUDENT ----------------
@app.route("/edit/<student_id>", methods=["GET", "POST"])
def edit_student(student_id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        department = request.form["department"]
        year = request.form["year"]
        email = request.form["email"]
        phone = request.form["phone"]

        cursor.execute("""
            UPDATE students
            SET
                name=?,
                department=?,
                year=?,
                email=?,
                phone=?
            WHERE student_id=?
        """, (
            name,
            department,
            year,
            email,
            phone,
            student_id
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("students"))

    cursor.execute("""
        SELECT student_id, name, department, year, email, phone
        FROM students
        WHERE student_id=?
    """, (student_id,))

    student = cursor.fetchone()

    conn.close()

    return render_template("edit_student.html", student=student)


# ---------------- DELETE STUDENT ----------------
@app.route("/delete/<student_id>")
def delete_student(student_id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE student_id=?",
        (student_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("students"))


# ---------------- VIEW ATTENDANCE ----------------
@app.route("/attendance")
def attendance():

    search_date = request.args.get("date", "")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if search_date:
        cursor.execute("""
            SELECT student_id, name, date, time, status
            FROM attendance
            WHERE date=?
            ORDER BY time DESC
        """, (search_date,))
    else:
        cursor.execute("""
            SELECT student_id, name, date, time, status
            FROM attendance
            ORDER BY date DESC, time DESC
        """)

    records = cursor.fetchall()
    conn.close()

    return render_template(
        "attendance.html",
        records=records,
        search_date=search_date
    )


# ---------------- CAPTURE FACE ----------------
@app.route("/capture/<student_id>")
def capture_face(student_id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT student_id, name FROM students WHERE student_id=?",
        (student_id,)
    )

    student = cursor.fetchone()

    conn.close()

    if student:
        capture_faces(student[0], student[1])

    return redirect(url_for("students"))


# ---------------- TRAIN MODEL ----------------
@app.route("/train")
def train_model():

    subprocess.run(
        [sys.executable, "backend/train_model.py"],
        check=True
    )

    return """
    <script>
        alert("✅ AI Model Trained Successfully!");
        window.location.href='/';
    </script>
    """

# ---------------- START ATTENDANCE ----------------
@app.route("/recognize")
def recognize():

    subprocess.Popen(
        [sys.executable, "backend/recognize_face.py"]
    )

    return """
    <script>
        alert("📷 Face Recognition Started!");
        window.location.href="/";
    </script>
    """
# ---------------- EXPORT ATTENDANCE ----------------
@app.route("/export")
def export_attendance():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT student_id, name, date, time, status
        FROM attendance
        ORDER BY date DESC, time DESC
    """)

    records = cursor.fetchall()
    conn.close()

    wb = Workbook()
    ws = wb.active
    ws.title = "Attendance"

    # Header
    ws.append([
        "Student ID",
        "Name",
        "Date",
        "Time",
        "Status"
    ])

    # Data
    for row in records:
        ws.append(row)

    filename = "Attendance_Report.xlsx"
    wb.save(filename)

    return send_file(
        filename,
        as_attachment=True
    )


# ---------------- SEND EMAIL ----------------
@app.route("/send_email")
def send_email():

    # Generate the latest attendance report
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT student_id, name, date, time, status
        FROM attendance
        ORDER BY date DESC, time DESC
    """)

    records = cursor.fetchall()
    conn.close()

    wb = Workbook()
    ws = wb.active
    ws.title = "Attendance"

    ws.append(["Student ID", "Name", "Date", "Time", "Status"])

    for row in records:
        ws.append(row)

    filename = "Attendance_Report.xlsx"
    wb.save(filename)

    # Send the report by email
    send_report()

    return """
    <script>
        alert("✅ Attendance report emailed successfully!");
        window.location.href="/";
    </script>
    """


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))  
# ---------------- START APP ----------------
if __name__ == "__main__":
    app.run(debug=False)