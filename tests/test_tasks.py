import pytest
from fastapi import status
from tests.test_auth_helper import test_company, test_user, auth_headers
from app.models.models import Task
from app.enums import TaskStatus


@pytest.fixture
def test_task(db_session, test_user):
    task = Task(
        summary="Test Task",
        description="Test Description",
        status=TaskStatus.TODO,
        priority="high",
        user_id=test_user.id
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task


def test_create_task_success(client, auth_headers):
    task_data = {
        "summary": "New Task",
        "description": "New Description",
        "status": "To do",
        "priority": "medium"
    }
    response = client.post("/api/v1/tasks/", json=task_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["summary"] == task_data["summary"]


def test_create_task_unauthorized(client, sample_task_data):
    response = client.post("/api/v1/tasks/", json=sample_task_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_tasks_success(client, test_task, auth_headers):
    response = client.get("/api/v1/tasks/", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_get_tasks_unauthorized(client):
    response = client.get("/api/v1/tasks/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_task_success(client, test_task, auth_headers):
    response = client.get(f"/api/v1/tasks/{test_task.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == test_task.id


def test_get_task_not_found(client, auth_headers):
    response = client.get("/api/v1/tasks/999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Task not found" in response.json()["detail"]


def test_get_task_unauthorized(client):
    response = client.get("/api/v1/tasks/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_task_success(client, test_task, auth_headers):
    update_data = {
        "summary": "Updated Task",
        "description": "Updated Description",
        "status": "In progress",
        "priority": "low"
    }
    response = client.put(f"/api/v1/tasks/{test_task.id}", json=update_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["summary"] == update_data["summary"]


def test_update_task_not_found(client, auth_headers):
    update_data = {"summary": "Updated Task"}
    response = client.put("/api/v1/tasks/999", json=update_data, headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_task_unauthorized(client, sample_task_data):
    response = client.put("/api/v1/tasks/1", json=sample_task_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_task_status_success(client, test_task, auth_headers):
    response = client.patch(f"/api/v1/tasks/{test_task.id}/status?status=Completed", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert "Task status updated successfully" in response.json()["message"]


def test_update_task_status_not_found(client, auth_headers):
    response = client.patch("/api/v1/tasks/999/status?status=Completed", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_task_status_unauthorized(client):
    response = client.patch("/api/v1/tasks/1/status?status=Completed")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED