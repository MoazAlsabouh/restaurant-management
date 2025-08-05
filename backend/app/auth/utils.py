import jwt
from datetime import datetime, timedelta
from flask import current_app
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

FRONTEND_URL = os.getenv('FRONTEND_URL')

def get_jwt_secret_key():
    try:
        return current_app.config["JWT_SECRET_KEY"]
    except RuntimeError:
        # fallback إذا لم يكن داخل التطبيق
        return os.getenv("JWT_SECRET_KEY", "default-fallback-secret")

def generate_token(user):
    payload = {
        "user_id": user.id,
        "email": user.email,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    secret = get_jwt_secret_key()
    token = jwt.encode(payload, secret, algorithm='HS256')
    return token

def decode_token(token):
    secret = get_jwt_secret_key()
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")

def generate_activation_token(user_id, expires_in=3600):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(seconds=expires_in)
    }
    secret = get_jwt_secret_key()
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token

def send_email(to_email, subject, body):
    smtp_server = os.getenv("MAIL_SERVER")
    smtp_port = int(os.getenv("MAIL_PORT", 587))
    smtp_user = os.getenv("MAIL_USERNAME")  # apikey
    smtp_pass = os.getenv("MAIL_PASSWORD")  # SendGrid API Key
    sender_name = os.getenv("MAIL_SENDER_NAME", "Syrian App")
    sender_email = os.getenv("MAIL_SENDER_EMAIL")

    msg = MIMEMultipart()
    msg["From"] = f"{sender_name} <{sender_email}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
            print(f"📨 تم إرسال الإيميل إلى {to_email}")
    except Exception as e:
        print(f"❌ فشل في إرسال الإيميل: {e}")

def send_email_verification_code(email, code):
    subject = "رمز التحقق من البريد الإلكتروني - Moaz Restaurant"
    body = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                background-color: #f9f9f9;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 40px auto;
                background-color: #ffffff;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                direction: rtl;
                text-align: right;
            }}
            .code {{
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                margin: 20px 0;
            }}
            .footer {{
                margin-top: 30px;
                font-size: 14px;
                color: #777;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>رمز التحقق</h2>
            <p>مرحبًا،</p>
            <p>رمز التحقق الخاص بك هو:</p>
            <div class="code">{code}</div>
            <p>إذا لم تطلب هذا الرمز، يرجى تجاهل هذه الرسالة.</p>
            <div class="footer">
                مع تحيات فريق Moaz Restaurant
            </div>
        </div>
    </body>
    </html>
    """
    send_email(email, subject, body)


def send_activation_link(email, token):
    activation_url = f"{FRONTEND_URL}/activate/{token}"
    subject = "تفعيل الحساب - Moaz Restaurant"
    body = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                background-color: #f9f9f9;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 40px auto;
                background-color: #ffffff;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                direction: rtl;
                text-align: right;
            }}
            .button {{
                display: inline-block;
                padding: 10px 20px;
                background-color: #27ae60;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 20px;
            }}
            .footer {{
                margin-top: 30px;
                font-size: 14px;
                color: #777;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>تفعيل حسابك</h2>
            <p>مرحبًا،</p>
            <p>يرجى الضغط على الزر أدناه لتفعيل حسابك:</p>
            <a href="{activation_url}" class="button">تفعيل الحساب</a>
            <p>إذا لم تطلب هذا الحساب، يرجى تجاهل هذه الرسالة.</p>
            <div class="footer">
                مع تحيات فريق Moaz Restaurant
            </div>
        </div>
    </body>
    </html>
    """
    send_email(email, subject, body)