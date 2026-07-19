import smtplib

EMAIL = "smartaiattendance2026@gmail.com"
APP_PASSWORD = "gotifgvkswfmejjx"

try:
    smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtp.login(EMAIL, APP_PASSWORD)
    print("SUCCESS")
    smtp.quit()
except Exception as e:
    print(e)