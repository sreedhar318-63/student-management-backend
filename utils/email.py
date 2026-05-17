import random
import string
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

# Mock OTP storage (In-memory)
otp_store = {}

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

def send_otp_email(receiver_email: str, otp: str):
    sender_email = os.getenv("SMTP_EMAIL")
    sender_password = os.getenv("SMTP_PASSWORD")
    
    # Save OTP to a file for easy access by the AI
    with open("latest_otp.txt", "w") as f:
        f.write(otp)

    # If no SMTP credentials, fallback to terminal output
    if not sender_email or not sender_password:
        print("\n" + "="*50)
        print(f"📧 EMAIL SENT TO: {receiver_email}")
        print(f"🔢 YOUR OTP IS: {otp}")
        print("⚠️ NOTE: Add SMTP_EMAIL and SMTP_PASSWORD to .env to send real emails.")
        print("="*50 + "\n")
        return True

    try:
        # Set up the email structure
        message = MIMEMultipart("alternative")
        message["Subject"] = "Password Reset OTP"
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the HTML version of your message
        html = f"""\
        <html>
          <body>
            <h2>Password Reset Request</h2>
            <p>You have requested to reset your password.</p>
            <p>Your One-Time Password (OTP) is: <strong><span style="font-size: 24px;">{otp}</span></strong></p>
            <p>If you didn't request this, please ignore this email.</p>
          </body>
        </html>
        """
        
        part = MIMEText(html, "html")
        message.attach(part)

        # Create secure connection with server and send email
        context = smtplib.SMTP("smtp.gmail.com", 587)
        context.starttls()
        context.login(sender_email, sender_password)
        context.sendmail(sender_email, receiver_email, message.as_string())
        context.quit()
        print(f"Real email successfully sent to {receiver_email}")
        return True
        
    except Exception as e:
        print(f"Failed to send email: {e}")
        # Fallback to console if real email fails
        print(f"OTP for {receiver_email} is: {otp}")
        return False
