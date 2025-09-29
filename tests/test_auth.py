import pytest
from fastapi import status
from tests.test_auth_helper import test_user, test_company
from app.auth import authenticate_user


def test_login_success(client, test_user):
    response = client.post("/token", data={
        "username": test_user.username,
        "password": "testpass"
    })
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    response = client.post("/token", data={
        "username": "invalid",
        "password": "invalid"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_wrong_password(client, test_user):
    response = client.post("/token", data={
        "username": test_user.username,
        "password": "wrongpassword"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_missing_credentials(client):
    response = client.post("/token", data={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_authenticate_user_success(db_session, test_user):
    user = authenticate_user(db_session, test_user.username, "testpass")
    assert user is not False
    assert user.username == test_user.username


def test_authenticate_user_invalid(db_session):
    user = authenticate_user(db_session, "invalid", "invalid")
    assert user is False