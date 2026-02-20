from fastapi.testclient import TestClient
from main import app
import os

# Create a test client
client = TestClient(app)

def test_api():
    print("Testing API Endpoints...")
    
    # 1. Test Root
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the AI Chatbot API"}
    print("- Root endpoint: SUCCESS")
    
    # 2. Test Signup
    signup_data = {
        "username": "testuser_api",
        "email": "test_api@example.com",
        "password": "testpassword"
    }
    response = client.post("/signup", json=signup_data)
    # 201 Created or 400 if already exists (depends on if DB was reset)
    if response.status_code == 201:
        assert response.json() == {"message": "User created successfully"}
        print("- Signup: SUCCESS")
    elif response.status_code == 400:
        print("- Signup: USER ALREADY EXISTS (Skipping creation)")
    else:
        assert False, f"Unexpected signup status code: {response.status_code}"
    
    # 3. Test Login
    login_data = {
        "email": "test_api@example.com",
        "password": "testpassword"
    }
    response = client.post("/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    print("- Login: SUCCESS")
    
    # 4. Test Invalid Login
    login_data_wrong = {
        "email": "test_api@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/login", json=login_data_wrong)
    assert response.status_code == 401
    print("- Invalid Login: SUCCESS (Correctly rejected)")

    print("\nAll API tests PASSED!")

if __name__ == "__main__":
    try:
        test_api()
    except Exception as e:
        print(f"API test failed: {e}")
        import traceback
        traceback.print_exc()
