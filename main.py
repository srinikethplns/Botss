import pandas as pd
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import schedule
import time

# Email Settings
EMAIL_ADDRESS = "srinikethplns890@gmail.com"
EMAIL_PASSWORD = "gqmw zmaa nafj jadt"
TO_EMAIL = "whitewolf1432@gmail.com"
EXCEL_PATH = "My to do list.xlsx"  # Replace with your Excel file name if it's on local
EXCEL_SHEET_LINK = "https://1drv.ms/x/c/7a6bfed5e1ad6060/EVRpn_N2zxhFueuz4Cv9UnwBku0LUBT9uLgqi-AuqkZlzg?e=ZZ916X"  # Editable OneDrive link

# Function to send task email
def send_task_email():
    today = datetime.now().strftime('%Y-%m-%d')
    try:
        # Read data from the Excel file
        df = pd.read_excel(EXCEL_PATH)  # Load your Excel file from local or OneDrive link

        # Create email body
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

        # Compose the email message
        message = f"📋 **Your Tasks for {today}**\n\n" + "\n".join(message_lines)

        if incomplete:
            message += f"\n\n⚠️ You missed these tasks: {', '.join(incomplete)}"
            message += "\n👉 Try harder tomorrow, or face consequences! 💢"
        
        message += f"\n\n🔗 **Edit your task list here:** {EXCEL_SHEET_LINK}"

        # Create MIMEText object for email
        msg = MIMEText(message)
        msg["Subject"] = f"Daily Checklist – {today}"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = TO_EMAIL

        # Send email via SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        print("[✓] Email sent successfully")

    except Exception as e:
        print(f"[!] Failed to send email: {e}")

# Schedule for daily email sending at 9 AM and 9 PM
schedule.every().day.at("09:00").do(send_task_email)   # Morning reminder
schedule.every().day.at("21:00").do(send_task_email)   # Evening follow-up

print("⏳ Bot is running...")

# Keep the bot running and check for scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(30)
