import pytest
from fastapi import status


def test_login_invalid_credentials(client):
    response = client.post("/token", data={
        "username": "invalid",
        "password": "invalid"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_missing_credentials(client):
    response = client.post("/token", data={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY