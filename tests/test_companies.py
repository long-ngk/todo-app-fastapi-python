import pytest
from fastapi import status
from tests.test_auth_helper import test_company, test_user, auth_headers, admin_headers, admin_user


def test_create_company_success(client, auth_headers):
    company_data = {
        "name": "New Company",
        "description": "New Description",
        "mode": "hybrid",
        "rating": 4
    }
    response = client.post("/api/v1/companies/", json=company_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == company_data["name"]


def test_create_company_unauthorized(client, sample_company_data):
    response = client.post("/api/v1/companies/", json=sample_company_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_companies_admin_success(client, test_company, admin_headers):
    response = client.get("/api/v1/companies/", headers=admin_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_companies_non_admin_forbidden(client, auth_headers):
    response = client.get("/api/v1/companies/", headers=auth_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "Only admin can view all companies" in response.json()["detail"]


def test_get_companies_unauthorized(client):
    response = client.get("/api/v1/companies/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_company_own_company(client, test_company, test_user, auth_headers):
    response = client.get(f"/api/v1/companies/{test_company.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == test_company.id


def test_get_company_other_company_forbidden(client, auth_headers):
    response = client.get("/api/v1/companies/999", headers=auth_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "You can only view your own company" in response.json()["detail"]


def test_get_company_admin_access(client, test_company, admin_headers):
    response = client.get(f"/api/v1/companies/{test_company.id}", headers=admin_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == test_company.id


def test_get_company_not_found(client, admin_headers):
    response = client.get("/api/v1/companies/999", headers=admin_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Company not found" in response.json()["detail"]


def test_get_company_unauthorized(client):
    response = client.get("/api/v1/companies/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED