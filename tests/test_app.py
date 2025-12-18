import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307  # Redirect
    assert response.headers["location"] == "/static/index.html"

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data
    assert "participants" in data["Basketball Team"]

def test_signup_success():
    response = client.post("/activities/Basketball%20Team/signup?email=test@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

def test_signup_duplicate():
    # First signup
    client.post("/activities/Basketball%20Team/signup?email=duplicate@example.com")
    # Second should fail
    response = client.post("/activities/Basketball%20Team/signup?email=duplicate@example.com")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data

def test_signup_invalid_activity():
    response = client.post("/activities/Invalid%20Activity/signup?email=test@example.com")
    assert response.status_code == 404

def test_unregister_success():
    # First signup
    client.post("/activities/Basketball%20Team/signup?email=unregister@example.com")
    # Then unregister
    response = client.post("/activities/Basketball%20Team/unregister?email=unregister@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

def test_unregister_not_signed_up():
    response = client.post("/activities/Basketball%20Team/unregister?email=notsigned@example.com")
    assert response.status_code == 400

def test_unregister_invalid_activity():
    response = client.post("/activities/Invalid%20Activity/unregister?email=test@example.com")
    assert response.status_code == 404