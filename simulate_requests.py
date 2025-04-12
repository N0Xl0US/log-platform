import requests
import time
import random

users = [
    {"username": "alice", "email": "alice@example.com"},
    {"username": "bob", "email": "bob@example.com"}
]

while True:
    action = random.choice(["login", "signup", "data", "profile"])
    user = random.choice(users)

    if action == "login":
        requests.post("http://localhost:8000/login", json=user)
    elif action == "signup":
        requests.post("http://localhost:8000/signup", json=user)
    elif action == "data":
        requests.get("http://localhost:8000/data")
    elif action == "profile":
        requests.put("http://localhost:8000/profile", json=user)
    print(f"Action: {action}, User: {user}")

    time.sleep(2)