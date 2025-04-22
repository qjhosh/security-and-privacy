import random
import string
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Generate random user accounts
def generate_users(n=10):
    users = {}
    for _ in range(n):
        account = ''.join(random.choices(string.digits, k=8))
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        users[account] = password
    return users

# Add test accounts
user_data = generate_users()
user_data["Group18"] = "12333444"
print("Generated User Accounts:", user_data)

# HTML template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Group 18 - Bank System</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; text-align: center; }
        header { background-color: #0044cc; padding: 20px; color: white; font-size: 24px; }
        .container {
            background: white; padding: 20px; margin: 50px auto; width: 300px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1); border-radius: 5px;
        }
        input, button {
            width: 100%; padding: 10px; margin: 10px 0; border-radius: 5px;
            border: 1px solid #ccc; font-size: 16px;
        }
        button {
            background-color: #0044cc; color: white; border: none; cursor: pointer;
        }
    </style>
</head>
<body>
    <header>Group 18 - Bank System</header>
    <section class="container">
        <h3>Login to Your Account</h3>
        <form method="POST" action="/login">
            <input type="text" name="account" placeholder="Enter Account Number" required>
            <input type="password" name="password" placeholder="Enter Password" required>
            <button type="submit">Login</button>
        </form>
        <p>{{ message|safe }}</p>
    </section>
    <section class="container">
        <h3>Register a New Account</h3>
        <form method="POST" action="/register">
            <input type="text" name="new_account" placeholder="Enter New Account Number" required>
            <input type="password" name="new_password" placeholder="Enter New Password" required>
            <button type="submit">Register</button>
        </form>
        <p>{{ register_message }}</p>
    </section>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_template, message="", register_message="")

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        print(f"Attempted Login - Account: {account}, Password: {password}")

        if account in user_data and user_data[account] == password:
            message = "Login Successful!<!--SUCCESS-->"
        else:
            message = "Invalid Credentials!<!--FAILED-->"
    
    return render_template_string(html_template, message=message, register_message="")

@app.route('/register', methods=['POST'])
def register():
    new_account = request.form['new_account']
    new_password = request.form['new_password']
    if new_account in user_data:
        register_message = "Account already exists!"
    else:
        user_data[new_account] = new_password
        register_message = "Registration Successful!"
    return render_template_string(html_template, message="", register_message=register_message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
