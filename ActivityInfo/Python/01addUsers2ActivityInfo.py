hi my name is kashif

import csv
import requests
import time

# ========== CONFIGURATIONS ==========

API_TOKEN = "XXXXXXXXXXXXXXXXXXX"
DATABASE_ID = "cqjj5vemfv8zsji3r"  # HPC.tools WIP Version 1 DB
# READONLY_ROLE_ID = "readonly"  
CM_ADM_ROLE_ID = "c2klv6bmewnkere2"
USERS_CSV_PATH = "users.csv"  # CSV with at least "name" and "email" columns

# Base URL for ActivityInfo API
BASE_URL = "https://3w.humanitarianaction.info/resources"  

# ========== FUNCTIONS ==========

def add_user_readonly(email, name):
    """
    Invite/add a user with readonly role to the database.
    """
    url = f"{BASE_URL}/databases/{DATABASE_ID}/users"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "email": email,
        "name": name,
        "scope": "DATABASE",
        "role": {
            "id": CM_ADM_ROLE_ID,   # e.g. "default" or "readonly"
            "parameters": {},
            "resources": []
        }
    }
    resp = requests.post(url, json=payload, headers=headers)
    if resp.status_code == 201:
        print(f"SUCCESS: {email} added as readonly")
        return True
    else:
        print(f"ERROR: Could not add {email} — status {resp.status_code}: {resp.text}")
        return False

def user_already_exists(email):
    """
    (Optional) Check if user with that email already has access.
    """
    url = f"{BASE_URL}/databases/{DATABASE_ID}/users"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise Exception(f"Could not fetch users from database: {resp.status_code} {resp.text}")
    users = resp.json()
    for u in users:
        if u.get("email", "").lower() == email.lower():
            return True
    return False

def main():
    with open(USERS_CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        # Expect CSV with two columns: name,email (with header row)
        header = next(reader)  # skip header row
        for row in reader:
            if len(row) < 2:
                print(f"Skipping invalid row: {row}")
                continue

            name = row[0].strip()
            email = row[1].strip()

            if not email or not name:
                print(f"Skipping row with missing name/email: {row}")
                continue

            # optional: check if already exists
            if user_already_exists(email):
                print(f"User {email} already in database — skipping.")
            else:
                success = add_user_readonly(email, name)
                time.sleep(0.5)

                
if __name__ == "__main__":
    main()
