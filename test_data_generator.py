import requests
import time
import random
from datetime import datetime
import json

# API endpoints
BASE_URL = "http://localhost:8000"
ENDPOINTS = {
    "general": ["/", "/data", "/nonexistent"],
    "auth": ["/login", "/signup", "/profile"]
}

# Sample user data for successful requests
VALID_USERS = [
    {"username": "john_doe", "email": "john@example.com"},
    {"username": "alice_smith", "email": "alice@example.com"},
    {"username": "bob_wilson", "email": "bob@example.com"},
    {"username": "emma_brown", "email": "emma@example.com"}
]

# Invalid data scenarios for failed requests
INVALID_DATA = [
    {},  # Empty payload
    {"username": "", "email": ""},  # Empty fields
    {"username": "test", "email": "invalid_email"},  # Invalid email
    {"username": "a" * 100, "email": "toolong@example.com"},  # Too long username
]

def generate_success_scenario(endpoint_type):
    if endpoint_type == "general":
        return ("GET", lambda url: requests.get(url))
    else:  # auth endpoints
        return ("POST", lambda url: requests.post(url, json=random.choice(VALID_USERS)))

def generate_failure_scenario():
    scenarios = [
        # Invalid JSON
        ("POST", lambda url: requests.post(url, data="invalid json")),
        # Missing required fields
        ("POST", lambda url: requests.post(url, json={})),
        # Invalid HTTP method
        ("PUT", lambda url: requests.put(url)),
        # Invalid query parameters
        ("GET", lambda url: requests.get(url + "?invalid=true")),
        # Invalid auth data
        ("POST", lambda url: requests.post(url, json=random.choice(INVALID_DATA))),
    ]
    return random.choice(scenarios)

def log_request_result(endpoint, response, request_type="success"):
    status = response.status_code
    success = 200 <= status < 400
    result = "SUCCESS" if success else "FAILURE"
    print(f"[{datetime.now()}] {request_type} request to {endpoint}: {status} ({result})")
    return success

def generate_logs():
    success_count = 0
    failure_count = 0
    
    while True:
        try:
            # Generate general logs
            for endpoint_type, endpoints in ENDPOINTS.items():
                for endpoint in endpoints:
                    full_url = f"{BASE_URL}{endpoint}"
                    
                    # Decide between success (70%) and failure (30%) scenario
                    if random.random() < 0.7:
                        method, request_func = generate_success_scenario(endpoint_type)
                    else:
                        method, request_func = generate_failure_scenario()
                    
                    try:
                        response = request_func(full_url)
                        if log_request_result(endpoint, response, method):
                            success_count += 1
                        else:
                            failure_count += 1
                            
                    except requests.exceptions.RequestException as e:
                        failure_count += 1
                        print(f"[{datetime.now()}] Error with {endpoint}: {str(e)}")
            
            # Print statistics
            total = success_count + failure_count
            if total > 0:
                success_rate = (success_count / total) * 100
                print(f"\nStatistics:")
                print(f"Success: {success_count} ({success_rate:.1f}%)")
                print(f"Failures: {failure_count} ({100-success_rate:.1f}%)")
                print(f"Total: {total}\n")
            
            # Wait for a random interval between 1-5 seconds
            time.sleep(random.uniform(1, 5))

        except KeyboardInterrupt:
            print("\nStopping log generation...")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    print("Starting log generation with mixed success/failure scenarios...")
    generate_logs() 