from auth import hash_password, verify_password, create_access_token, verify_token
import time

def test_auth():
    print("Testing Authentication Functions...")
    
    # 1. Test Password Hashing
    password = "secret_password"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False
    print("- Password hashing and verification: SUCCESS")
    
    # 2. Test JWT Token
    user_data = {"sub": "testuser", "email": "test@example.com"}
    token = create_access_token(user_data)
    assert isinstance(token, str)
    
    payload = verify_token(token)
    assert payload["sub"] == "testuser"
    assert payload["email"] == "test@example.com"
    assert "exp" in payload
    print("- JWT token creation and verification: SUCCESS")
    
    print("\nAll authentication tests PASSED!")

if __name__ == "__main__":
    try:
        test_auth()
    except Exception as e:
        print(f"Auth test failed: {e}")
