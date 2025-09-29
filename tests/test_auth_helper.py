import pytest
from app.auth import get_password_hash, verify_password, create_access_token
from app.models.models import User, Company
from datetime import timedelta


@pytest.fixture
def test_company(db_session):
    company = Company(name="Test Company", description="Test", mode="remote", rating=5)
    db_session.add(company)
    db_session.commit()
    db_session.refresh(company)
    return company


@pytest.fixture
def test_user(db_session, test_company):
    hashed_password = get_password_hash("testpass")
    user = User(
        email="test@example.com",
        username="testuser",
        first_name="Test",
        last_name="User",
        hashed_password=hashed_password,
        is_active=True,
        is_admin=False,
        company_id=test_company.id
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def admin_user(db_session, test_company):
    hashed_password = get_password_hash("adminpass")
    user = User(
        email="admin@example.com",
        username="admin",
        first_name="Admin",
        last_name="User",
        hashed_password=hashed_password,
        is_active=True,
        is_admin=True,
        company_id=test_company.id
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user):
    token = create_access_token(data={"sub": test_user.username})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(admin_user):
    token = create_access_token(data={"sub": admin_user.username})
    return {"Authorization": f"Bearer {token}"}


def test_password_hashing():
    password = "testpassword"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False


def test_create_access_token():
    data = {"sub": "testuser"}
    token = create_access_token(data)
    assert isinstance(token, str)
    assert len(token) > 0
    
    # Test with expiration
    token_with_exp = create_access_token(data, expires_delta=timedelta(minutes=30))
    assert isinstance(token_with_exp, str)
    assert len(token_with_exp) > 0