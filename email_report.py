import smtplib
from email.message import EmailMessage
import os

# ==========================
# Gmail Settings
# ==========================
SENDER_EMAIL = "smartaiattendance@gmail.com"
APP_PASSWORD = "gotifgvkswfmejjx"

# Email to receive the report
RECEIVER_EMAIL = "smartaiattendance@gmail.com"


def send_report():

    filename = "Attendance_Report.xlsx"

    if not os.path.exists(filename):
        print("Attendance report not found.")
        return

    msg = EmailMessage()

    msg["Subject"] = "Smart AI Attendance Report"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    msg.set_content(
        """
Hello,

Please find the attached Smart AI Attendance Report.

Regards,
Smart AI Attendance System
"""
    )

    with open(filename, "rb") as f:
        file_data = f.read()

    msg.add_attachment(
        file_data,
        maintype="application",
        subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=filename
    )

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)

        print("Email sent successfully!")

    except Exception as e:
        print("Email sending failed.")
        print(e)


# Test the file directly
if __name__ == "__main__":
    send_report()