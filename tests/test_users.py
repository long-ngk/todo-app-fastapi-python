import pytest
from fastapi import status


def test_create_user(client, sample_user_data):
    response = client.post("/api/v1/users/", json=sample_user_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY  # Missing company


def test_get_current_user_unauthorized(client):
    response = client.get("/api/v1/users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_users_unauthorized(client):
    response = client.get("/api/v1/users/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED