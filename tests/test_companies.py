import pytest
from fastapi import status


def test_create_company(client, sample_company_data):
    response = client.post("/api/v1/companies/", json=sample_company_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_companies_unauthorized(client):
    response = client.get("/api/v1/companies/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_company_unauthorized(client):
    response = client.get("/api/v1/companies/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED