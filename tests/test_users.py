import pytest
from fastapi import status
from tests.test_auth_helper import test_company, test_user, auth_headers


def test_create_user_success(client, test_company):
    user_data = {
        "email": "newuser@example.com",
        "username": "newuser",
        "first_name": "New",
        "last_name": "User",
        "password": "password123",
        "company_id": test_company.id
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == user_data["email"]
    assert response.json()["username"] == user_data["username"]


def test_create_user_duplicate_email(client, test_company, test_user):
    user_data = {
        "email": test_user.email,
        "username": "differentuser",
        "first_name": "Different",
        "last_name": "User",
        "password": "password123",
        "company_id": test_company.id
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Email already registered" in response.json()["detail"]


def test_get_current_user_success(client, test_user, auth_headers):
    response = client.get("/api/v1/users/me", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == test_user.email
    assert response.json()["username"] == test_user.username


def test_get_current_user_unauthorized(client):
    response = client.get("/api/v1/users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_users_success(client, test_user, auth_headers):
    response = client.get("/api/v1/users/", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_users_unauthorized(client):
    response = client.get("/api/v1/users/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED