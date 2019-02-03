from flask import json

from api.helpers.responses import wrong_status, invalid_token_message
from .base import user1_header, admin_header


# EDIT A RED-FLAG RECORD'S STATUS
def test_edit_a_red_flag_status_without_a_token(client):
    response = client.patch(
        "api/v3/red-flags/10df0c67-5f2b-4e5d-8b45-7357bbf3bebb/status"
    )
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data["status"] == 401
    assert data["error"] == invalid_token_message


def test_non_admin_edit_a_red_flag_status(client):
    response = client.patch(
        "api/v3/red-flags/10df0c67-5f2b-4e5d-8b45-7357bbf3bebb/status",
        headers=user1_header,
        data=json.dumps({"status": "resolved"}),
    )
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data["status"] == 401
    assert data["error"] == "Only Admin can access this resource"


def test_edit_a_red_flag_status_with_an_invalid_red_flag_id(client):
    response = client.patch(
        "api/v3/red-flags/f/status",
        headers=admin_header,
        data=json.dumps({"status": "resolved"}),
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == "Invalid incident id"


#
def test_edit_a_red_flag_status_without_request_data(client):
    response = client.patch(
        "api/v3/red-flags/10df0c67-5f2b-4e5d-8b45-7357bbf3bebb/status",
        headers=admin_header,
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == "Please provide valid input data"


def test_edit_a_red_flag_status_with_invalid_status_data(client):
    response = client.patch(
        "api/v3/red-flags/10df0c67-5f2b-4e5d-8b45-7357bbf3bebb/status",
        headers=admin_header,
        data=json.dumps({"status": "I disagree"}),
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == wrong_status

    response = client.patch(
        "api/v3/red-flags/10df0c67-5f2b-4e5d-8b45-7357bbf3bebb/status",
        headers=admin_header,
        data=json.dumps({"status": 3}),
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == wrong_status


def test_edit_a_red_flag_status_for_a_red_flag_record_which_does_not_exist(
    client
):
    response = client.patch(
        "api/v3/red-flags/10df0c67-5f2b-4e5d-8b45-7357ebf3bfbb/status",
        headers=admin_header,
        data=json.dumps({"status": "rejected"}),
    )
    assert response.status_code == 404
    data = json.loads(response.data.decode())
    assert data["status"] == 404
    assert data["error"] == "red-flag record with specified id does not exist"


def test_edit_a_red_flag_status(client):
    response = client.patch(
        "api/v3/red-flags/b7e7ddf0-3bdb-4932-888d-e262a54bda6a/status",
        headers=admin_header,
        data=json.dumps({"status": "resolved"}),
    )

    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["status"] == 200
    assert data["data"][0]["success"] == "Updated red-flag record’s status"
    assert data["data"][0]["status"] == "Resolved"


def test_edit_a_intervention_status(client):
    response = client.patch(
        "api/v3/interventions/79cc7006-224e-4e0c-8253-117305466b4a/status",
        headers=admin_header,
        data=json.dumps({"status": "resolved"}),
    )

    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["status"] == 200
    assert data["data"][0]["success"] == "Updated intervention record’s status"
    assert data["data"][0]["status"] == "Resolved"
