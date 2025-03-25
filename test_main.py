# test_main.py
import pytest
from main import app


@pytest.fixture
def client():
    """
    Pytest fixture that creates a Flask test client from the 'app' in main.py.
    """
    with app.test_client() as client:
        yield client


def test_root_endpoint(client):
    """
    Test the GET '/' endpoint to ensure it returns
    the greeting and a 200 status code.
    """
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Hello from my Password Validator!" in resp.data


def test_root_endpoint(client):
    """
    Test the GET '/' endpoint to ensure it returns
    the greeting and a 200 status code.
    """
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Hello from my Password Validator!" in resp.data


def test_password_too_short(client):
    resp = client.post("/v1/checkPassword", json={"password": "Ab1!"})
    assert resp.status_code == 400
    assert resp.get_json()["reason"] == "Password must be at least 8 characters long"


def test_password_missing_uppercase(client):
    resp = client.post("/v1/checkPassword", json={"password": "password1!"})
    assert resp.status_code == 400
    assert resp.get_json()["reason"] == "Password must contain at least one uppercase letter"


def test_password_missing_lowercase(client):
    resp = client.post("/v1/checkPassword", json={"password": "PASSWORD1!"})
    assert resp.status_code == 400
    assert resp.get_json()["reason"] == "Password must contain at least one lowercase letter"


def test_password_missing_digit(client):
    resp = client.post("/v1/checkPassword", json={"password": "Password!"})
    assert resp.status_code == 400
    assert resp.get_json()["reason"] == "Password must contain at least one digit"


def test_password_missing_special_character(client):
    resp = client.post("/v1/checkPassword", json={"password": "Password123"})
    assert resp.status_code == 400
    assert resp.get_json()["reason"] == "Password must contain at least one special character"


def test_password_valid(client):
    resp = client.post("/v1/checkPassword", json={"password": "Password123!"})
    assert resp.status_code == 200
    assert resp.get_json()["valid"] is True