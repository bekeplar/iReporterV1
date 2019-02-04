from flask import json
from .base import admin_header, user1_header, user1_id


def test_invalid_url(client):
    response = client.delete("api/v2/")
    assert response.status_code == 404
    data = json.loads(response.data.decode())
    assert data["error"] == "Endpoint for specified URL does not exist"

    response = client.get("api/v1/red-flag/ssd", headers=user1_header)
    assert response.status_code == 404
    data = json.loads(response.data.decode())
    assert data["error"] == "Endpoint for specified URL does not exist"


def test_method_not_allowed(client):
    response = client.delete("/")
    assert response.status_code == 405
    data = json.loads(response.data.decode())
    assert data["error"] == "Method not allowed"


def test_welcome_message(client):
    response = client.get("/")
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["message"] == "Welcome to iReporter API V3"
    assert data["status"] == 200
