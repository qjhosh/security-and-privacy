import random
import string
import time

# 生成随机用户账户
def generate_users(n=10):
    users = {
        "chen": {
            "password": "123",
            "email": "jiahuiqinjh@gmail.com"
        }
    }  # 预设账户
    for _ in range(n):
        account = ''.join(random.choices(string.digits, k=8))
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        email = 'jiahuiqinjh@gmail.com'
        users[account] = {
            "password": password,
            "email": email
        }
    return users

# 全局用户数据库
user_data = generate_users()
failed_attempts = {}
account_locks = {}
print("Generated User Accounts:", user_data)
def check_account_lock(account):
    """检查账户是否被锁定"""
    if account in account_locks:
        if time.time() - account_locks[account] < 600:
            return True
        del account_locks[account]  # 解除锁定
    return False

def record_failed_attempt(account):
    """记录失败尝试并锁定账户"""
    failed_attempts[account] = failed_attempts.get(account, 0) + 1
    if failed_attempts[account] >= 3:
        account_locks[account] = time.time()
        return True
    return False
