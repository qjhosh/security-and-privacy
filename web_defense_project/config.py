import os
import secrets

class Config:
    SECRET_KEY = secrets.token_hex(32)

    # Flask-Session 配置
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False

    # 自动创建 session 文件夹，确保 Flask-Session 可以存储数据
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SESSION_FILE_DIR = os.path.join(BASE_DIR, "session_data")

    if not os.path.exists(SESSION_FILE_DIR):
        os.makedirs(SESSION_FILE_DIR)


    # Google reCAPTCHA 配置
    RECAPTCHA_SITE_KEY = "6LcgPfYqAAAAAAZgFvsKL3WiL21qlJy9p5TK9Jkc"
    RECAPTCHA_SECRET_KEY = "6LcgPfYqAAAAAE2goieMi-L0Y8sRQTujEtQWQBBn"

    # Flask-Mail 配置 (使用 QQ 邮箱)
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = "2422128106@qq.com"
    MAIL_PASSWORD = "etglletwdiiwecda"
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
