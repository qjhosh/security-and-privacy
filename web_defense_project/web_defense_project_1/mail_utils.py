from flask_mail import Mail, Message

mail = None

def init_mail(app):
    """初始化 Flask-Mail"""
    global mail
    mail = Mail(app)

def send_otp_email(email, otp_code):
    """发送 OTP 邮件"""
    if not mail:
        raise ValueError("Mail is not initialized!")

    msg = Message("Your OTP Code", recipients=[email])
    msg.body = f"Your one-time password (OTP) is: {otp_code}. It is valid for 5 minutes."
    mail.send(msg)

