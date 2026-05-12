import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"

def test_auth():
    print("Testing Auth Endpoints...")
    try:
        res = requests.get(f"{BASE_URL}/health", timeout=5)
        print("Health Check:", res.json())
    except Exception as e:
        print("Server not running or didn't respond in time:", e)
        return

    test_email = "testuser_test2@example.com"
    test_password = "password123"
    test_name = "Test User"
    test_dosha = "vata"

    print("\n--- Testing Signup ---")
    signup_data = {
        "name": test_name,
        "email": test_email,
        "password": test_password,
        "dosha": test_dosha
    }
    
    response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    print("\n--- Testing Login ---")
    login_data = {
        "email": test_email,
        "password": test_password
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    test_auth()
