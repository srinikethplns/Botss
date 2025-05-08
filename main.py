import pandas as pd
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import pytz
import time

# Email Settings
EMAIL_ADDRESS = "srinikethplns890@gmail.com"
EMAIL_PASSWORD = "gqmw zmaa nafj jadt"
TO_EMAIL = "whitewolf1432@gmail.com"
EXCEL_PATH = "My to do list.xlsx"
EXCEL_SHEET_LINK = "https://1drv.ms/x/c/7a6bfed5e1ad6060/EVRpn_N2zxhFueuz4Cv9UnwBku0LUBT9uLgqi-AuqkZlzg?e=ZZ916X"

# Set IST timezone
IST = pytz.timezone('Asia/Kolkata')

# Function to send task email
def send_task_email():
    today = datetime.now(IST).strftime('%Y-%m-%d')
    try:
        df = pd.read_excel(EXCEL_PATH)

        message_lines = []
        incomplete = []

        for _, row in df.iterrows():
            task = row['Task']
            status = str(row.get('Status', '')).strip().lower()
            if status == 'done':
                message_lines.append(f"✔️ {task}")
            else:
                message_lines.append(f"❌ {task}")
                incomplete.append(task)

        message = f"📋 **Your Tasks for {today}**\n\n" + "\n".join(message_lines)

        if incomplete:
            message += f"\n\n⚠️ You missed these tasks: {', '.join(incomplete)}"
            message += "\n👉 Try harder tomorrow, or face consequences! 💢"
        
        message += f"\n\n🔗 **Edit your task list here:** {EXCEL_SHEET_LINK}"

        msg = MIMEText(message)
        msg["Subject"] = f"Daily Checklist – {today}"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = TO_EMAIL

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"[✓] Email sent at {datetime.now(IST).strftime('%H:%M:%S')}")

    except Exception as e:
        print(f"[!] Failed to send email: {e}")

# Track whether emails were sent today
sent_flags = {"09:00": False, "21:00": False}
print("⏳ Bot is running...")

while True:
    now_ist = datetime.now(IST)
    current_time = now_ist.strftime("%H:%M")

    if current_time in sent_flags and not sent_flags[current_time]:
        send_task_email()
        sent_flags[current_time] = True

    # Reset the flags just after midnight
    if now_ist.strftime("%H:%M") == "00:01":
        sent_flags = {"09:00": False, "21:00": False}

    time.sleep(30)
