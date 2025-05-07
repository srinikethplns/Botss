import smtplib
from email.mime.text import MIMEText

# Your credentials
EMAIL_ADDRESS = "srinikethplns890@gmail.com"  # Your email address
EMAIL_PASSWORD = "gqmw zmaa nafj jadt"  # Your email app password (not your regular Gmail password)
TO_EMAIL = "whitewolf1432@gmail.com"  # The email address where the email will be sent

# Create the email message
subject = "Test Email from Python"
body = "This is a test email sent from Python using smtplib."

msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = EMAIL_ADDRESS
msg["To"] = TO_EMAIL

# Set up the SMTP server (Gmail)
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # Use TLS (Transport Layer Security)
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # Log in to your email account
        server.send_message(msg)  # Send the email
        print("Test email sent successfully!")

except Exception as e:
    print(f"Failed to send email: {e}")

