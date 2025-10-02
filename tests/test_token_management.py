import pytest
from datetime import datetime, timedelta
from src.modules.token import TokenManagement

SECRET = "testsecret123"
EXPIRY_MINUTES = 1*60

@pytest.fixture
def token_manager():
    return TokenManagement(secret_key=SECRET, expiry_minutes=EXPIRY_MINUTES)

@pytest.mark.parametrize(
    "token_data",
    [
        {"user_id": "1", "role": "admin"},
        {"user_id": "2", "role": "user"},
        {"user_id": "3", "role": "guest"}
    ]
)
def test_generate_and_validate_token(token_manager, token_data):
    # Generate token
    token = token_manager.generate_token(token_data)
    assert token is not None
    assert isinstance(token, str)

    # Validate token
    validated_data = token_manager.validate_token(token)
    assert validated_data["user_id"] == token_data["user_id"]
    assert validated_data["role"] == token_data["role"]

def test_invalid_token(token_manager):
    invalid_token = "abcd.invalid.token"
    assert token_manager.validate_token(invalid_token) is None
