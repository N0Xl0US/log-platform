import requests
import time
import random
from datetime import datetime
import json

# API endpoints
BASE_URL = "http://localhost:8000"
ENDPOINTS = {
    "general": ["/", "/data"],
    "auth": ["/login", "/signup"]
}

# Sample user data
USERS = [
    {"username": "john_doe", "email": "john@example.com"},
    {"username": "alice_smith", "email": "alice@example.com"},
    {"username": "bob_wilson", "email": "bob@example.com"},
    {"username": "emma_brown", "email": "emma@example.com"}
]

def generate_logs():
    while True:
        try:
            # Generate general logs
            for endpoint in ENDPOINTS["general"]:
                response = requests.get(f"{BASE_URL}{endpoint}")
                print(f"General log generated for {endpoint}: {response.status_code}")

            # Generate auth logs
            for endpoint in ENDPOINTS["auth"]:
                user = random.choice(USERS)
                response = requests.post(
                    f"{BASE_URL}{endpoint}",
                    json=user
                )
                print(f"Auth log generated for {endpoint}: {response.status_code}")

            # Wait for a random interval between 1-5 seconds
            time.sleep(random.uniform(1, 5))

        except requests.exceptions.RequestException as e:
            print(f"Error generating logs: {e}")
            time.sleep(5)  # Wait before retrying if there's an error

if __name__ == "__main__":
    print("Starting log generation...")
    generate_logs() 