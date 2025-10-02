import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from src.config import Config
from src.modules.token import TokenManagement
from main import app  # your FastAPI app with router_registry.register_routes()

@pytest.fixture
def test_app():
    return app

@pytest.mark.asyncio
async def test_generate_token_route(test_app):
    async with AsyncClient(app=test_app, base_url="http://testserver") as client:
        response = await client.post("/token/generate", json={"token_data": {"user_id": "u1"}})
        assert response.status_code == 201
        data = response.json()["data"]
        assert "access_token" in data
        # Also check cookie is set
        assert "access_token" in response.cookies

@pytest.mark.asyncio
async def test_validate_token_route(test_app):
    async with AsyncClient(app=test_app, base_url="http://testserver") as client:
        # Generate token first
        response = await client.post("/token/generate", json={"token_data": {"user_id": "u1"}})
        token = response.json()["data"]["access_token"]

        # Validate using header
        validate_resp = await client.post("/token/validate", headers={"Authorization": f"Bearer {token}"})
        assert validate_resp.status_code == 200
        assert validate_resp.json()["data"]["user_id"] == "u1"

        # Validate using cookie
        cookies = {"access_token": token}
        validate_cookie_resp = await client.post("/token/validate", cookies=cookies)
        assert validate_cookie_resp.status_code == 200
        assert validate_cookie_resp.json()["data"]["user_id"] == "u1"
