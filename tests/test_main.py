import pytest
from fastapi import status


def test_read_root(client):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Welcome to Todo App API"}