import pytest
from fastapi import status


def test_create_task_unauthorized(client, sample_task_data):
    response = client.post("/api/v1/tasks/", json=sample_task_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_tasks_unauthorized(client):
    response = client.get("/api/v1/tasks/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_task_unauthorized(client):
    response = client.get("/api/v1/tasks/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_task_unauthorized(client, sample_task_data):
    response = client.put("/api/v1/tasks/1", json=sample_task_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_task_status_unauthorized(client):
    response = client.patch("/api/v1/tasks/1/status", json="Completed")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED