from flask import Flask, render_template, request, session, jsonify, redirect, url_for
from flask_session import Session
from flask_mail import Mail
import random
import pyotp
import qrcode
import io
import base64
import time
import requests
from config import Config
from mail_utils import init_mail, send_otp_email
from users import user_data, check_account_lock, record_failed_attempt

app = Flask(__name__)
app.config.from_object(Config)
Session(app)
init_mail(app)

def generate_captcha():
    """生成数字 CAPTCHA"""
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    session["captcha_answer"] = num1 + num2  # 存储正确答案
    return f"{num1} + {num2} = ?"
def generate_qr(pending_user):
    otp_uri = pyotp.TOTP(pending_user["otp_secret"]).provisioning_uri(
        name=pending_user["account"], issuer_name="SecureApp"
    )
    img = qrcode.make(otp_uri)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

@app.route('/')
def home():
    """登录页面"""
    captcha_question = generate_captcha()
    return render_template("login.html", captcha_question=captcha_question, message="")

@app.route('/register')
def register_page():
    """注册页面"""
    return render_template("register.html", recaptcha_site_key=app.config["RECAPTCHA_SITE_KEY"], message="")

@app.route('/login', methods=['POST'])
def login():
    """处理登录请求"""
    account = request.form.get("account")
    password = request.form.get("password")
    user_captcha = request.form.get("captcha")

    if "captcha_answer" not in session or not user_captcha or int(user_captcha) != session["captcha_answer"]:
        return render_template("login.html", message="⚠️Invalid CAPTCHA!", captcha_question=generate_captcha())

    if check_account_lock(account):
        # return jsonify({"message": "Account locked. Try again later."}), 403
        return render_template("login.html", message="⚠️ Account locked. Try again later.",
                           captcha_question=generate_captcha())

    if account in user_data and user_data[account]["password"] == password:
        session["user_account"] = account
        return redirect(url_for('otp_verification'))

    if record_failed_attempt(account):
        return render_template("login.html", message="⚠️ Too many failed attempts. Account locked.",
                               captcha_question=generate_captcha())

    return render_template("login.html", message="⚠️ Incorrect account or password.", captcha_question=generate_captcha())

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_account = request.form["new_account"]
        new_password = request.form["new_password"]
        new_email = request.form["new_email"] 
        recaptcha_response = request.form.get("g-recaptcha-response")

        # ✅ Step 1: 验证 reCAPTCHA
        recaptcha_verify_url = "https://www.google.com/recaptcha/api/siteverify"
        recaptcha_payload = {
            "secret": app.config["RECAPTCHA_SECRET_KEY"],
            "response": recaptcha_response
        }
        recaptcha_result = requests.post(recaptcha_verify_url, data=recaptcha_payload).json()

        if not recaptcha_result.get("success"):
            return render_template("register.html", message="reCAPTCHA verification failed!",
                                   recaptcha_site_key=app.config["RECAPTCHA_SITE_KEY"])

        if new_account in user_data:
            return render_template("register.html", message="Account already exists!",
                                   recaptcha_site_key=app.config["RECAPTCHA_SITE_KEY"])

        # ✅ Step 2: 创建 TOTP 密钥 + 暂存信息到 session
        otp_secret = pyotp.random_base32()
        session["pending_user"] = {
            "account": new_account,
            "password": new_password,
            "email": new_email,
            "otp_secret": otp_secret
        }

        # ✅ 生成二维码 base64
        otp_uri = pyotp.TOTP(otp_secret).provisioning_uri(name=new_account, issuer_name="SecureApp")
        img = qrcode.make(otp_uri)
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()

        # ✅ 渲染到 TOTP 验证页面
        return render_template("verify_totp.html", qr=qr_base64, otp_secret=otp_secret)

    return render_template("register.html", recaptcha_site_key=app.config["RECAPTCHA_SITE_KEY"])

@app.route('/verify_totp', methods=['POST'])
def verify_totp():
    user_input = request.form.get("totp")
    pending = session.get("pending_user")

    if not pending:
        return redirect(url_for("register"))

    totp = pyotp.TOTP(pending["otp_secret"])
    if totp.verify(user_input):
        # ✅ 验证通过 → 真正保存
        user_data[pending["account"]] = {
            "password": pending["password"],
            "email": pending["email"],
            "otp_secret": pending["otp_secret"]
        }
        session.pop("pending_user")
        print(f"✅ New user registered: {pending['account']} with TOTP")
        return redirect(url_for('home', register_success="True"))

    # ❌ 验证失败
    return render_template("verify_totp.html", qr=generate_qr(pending), otp_secret=pending["otp_secret"],
                           message="❌ Invalid TOTP Code")

# ✅ OTP 验证页面
@app.route('/otp_verification', methods=['GET', 'POST'])
def otp_verification():
    """OTP 认证页面"""
    account = session.get("user_account")  # 登录成功后保存在 session 中

    if not account or account not in user_data:
        return redirect(url_for('home'))

    registered_email = user_data[account]["email"]

    if request.method == 'POST':
        user_otp = request.form.get("otp")

        # 检查 OTP 是否过期（5 分钟）
        if "otp" not in session or time.time() - session["otp_time"] > 300:
            return render_template("otp_verification.html", message="⚠️ OTP expired. Please resend.", email=registered_email)

        if user_otp == session["otp"]:
            return render_template("login.html", message="✅ Login Successful!",captcha_question=generate_captcha())

        return render_template("otp_verification.html", message="⚠️ Invalid OTP.", email=registered_email)

    return render_template("otp_verification.html", message="", email=registered_email)

# ✅ 生成 OTP 并发送邮件
@app.route('/send_otp', methods=['POST'])
def send_otp():
    """发送 OTP 验证码"""
    account = session.get("user_account")
    if not account or account not in user_data:
        return jsonify({"message": "⚠️ Session invalid. Please login again."}), 400

    email = user_data[account]["email"]


    otp_code = str(random.randint(100000, 999999))  # 生成 6 位随机 OTP
    session["otp"] = otp_code
    session["otp_time"] = time.time()  # 记录 OTP 生成时间

    send_otp_email(email, otp_code)  # 发送 OTP 邮件
    return jsonify({"message": "✅ OTP sent successfully!"})


@app.route('/otp_totp', methods=['GET', 'POST'])
def otp_totp():
    account = session.get("user_account")
    if not account or account not in user_data:
        return redirect(url_for("home"))

    if request.method == 'POST':
        code = request.form.get("totp")
        totp = pyotp.TOTP(user_data[account]["otp_secret"])
        if totp.verify(code):
            return render_template("login.html", message="✅ Login successful!", captcha_question=generate_captcha())
        else:
            return render_template("otp_totp.html", message="❌ Invalid TOTP code")

    return render_template("otp_totp.html", message="")

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
