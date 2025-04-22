import requests
import base64
import random
import string
import schedule
import time
from datetime import datetime

# GitHub token and repo info
token = "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"
repo = "termux7788/new"
path = "file.txt"

# GitHub API headers
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

def random_text(length=20):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def update_file():
    print(f"[{datetime.now()}] Running update_file task...")

    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    response = requests.get(url, headers=headers)
    new_content = random_text()

    if response.status_code == 200:
        file_data = response.json()
        sha = file_data["sha"]

        data = {
            "message": "Overwrite file with new random text",
            "content": base64.b64encode(new_content.encode()).decode(),
            "sha": sha
        }

        update_response = requests.put(url, headers=headers, json=data)
        print("File overwritten:", update_response.status_code, update_response.json())

    elif response.status_code == 404:
        data = {
            "message": "Create new file with random text",
            "content": base64.b64encode(new_content.encode()).decode()
        }

        create_response = requests.put(url, headers=headers, json=data)
        print("File created:", create_response.status_code, create_response.json())

    else:
        print("Error checking file:", response.status_code, response.json())

# Schedule the task for every day at 10:00 AM
schedule.every().day.at("10:00").do(update_file)

# Main loop
print("Bot is running. Waiting for scheduled time...")

while True:
    schedule.run_pending()
    time.sleep(30)
