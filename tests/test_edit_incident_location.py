from flask import json

from api.helpers.responses import invalid_token_message
from .base import user2_header, user1_header

# EDIT A RED-FLAG RECORD'S LOCATION
def test_edit_a_red_flag_location_without_a_token(client):
    response = client.patch(
        "api/v3/red-flags/10df0c67-5f2b-4e5d-8b45-7357bbf3bebb/location",
        data=json.dumps({"location": [12, 12]}),
    )
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data["status"] == 401
    assert data["error"] == invalid_token_message


def test_edit_a_red_flag_location_without_location_data(client):
    response = client.patch(
        "api/v3/red-flags/10df0c67-5f2b-4e5d-8b45-7357bbf3bebb/location",
        headers=user1_header,
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == "Please provide valid input data"


def test_edit_a_red_flag_location_which_does_not_exist(client):
    response = client.patch(
        "api/v3/red-flags/10df0c37-5f2b-4e5d-8b45-7357bbf3bebb/location",
        headers=user1_header,
        data=json.dumps({"location": [12, 12]}),
    )
    assert response.status_code == 404
    data = json.loads(response.data.decode())
    assert data["status"] == 404
    assert data["error"] == "red-flag record with specified id does not exist"


def test_edit_a_red_flag_location_which_does_not_belong_to_user(client):
    response = client.patch(
        "api/v3/red-flags/10df0c67-5f2b-4e5d-8b45-7357bbf3bebb/location",
        headers=user2_header,
        data=json.dumps({"location": [12, 12]}),
    )
    assert response.status_code == 403
    data = json.loads(response.data.decode())
    assert data["status"] == 403
    assert data["error"] == "You are not allowed to modify this resource"


def test_edit_a_red_flag_location_with_invalid_red_flag_id(client):
    response = client.patch(
        "api/v3/red-flags/df/location",
        headers=user2_header,
        data=json.dumps({"location": [12, 12]}),
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == "Invalid incident id"


def test_edit_a_red_flag_location_status_of_draft(client):
    response = client.patch(
        "api/v3/red-flags/10df0c67-5f2b-4e5d-8b45-7357bbf3bebb/location",
        headers=user1_header,
        data=json.dumps({"location": [12, 12]}),
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["status"] == 200
    assert data["data"][0]["success"] == "Updated red-flag record’s location"
    assert data["data"][0]["id"] == "10df0c67-5f2b-4e5d-8b45-7357bbf3bebb"


def test_edit_a_red_flag_location_with_invalid_location_coordinates(client):
    response = client.patch(
        "api/v3/red-flags/10df0c67-5f2b-4e5d-8b45-7357bbf3bebb/location",
        headers=user1_header,
        data=json.dumps({"location": [-90, 12]}),
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == (
        "latitude must be between -90 and 90 and longitude"
        " coordinates must be between -180 and 180"
    )


def test_edit_a_red_flag_location_status_other_than_draft(client):
    response = client.patch(
        "api/v3/red-flags/df57bf19-1495-40aa-bbc3-5cc792a8f8f2/location",
        headers=user1_header,
        data=json.dumps({"location": [12, 12]}),
    )
    assert response.status_code == 403
    data = json.loads(response.data.decode())
    assert data["status"] == 403
    assert data["error"] == "You are not allowed to modify this resource"


# TEST EDIT INTERVENTION RECORD'S LOCATION
def test_edit_a_intervention_location_without_a_token(client):
    response = client.patch(
        "api/v3/interventions/79bb7006-272e-4e0c-8253-117305466b4a/location",
        data=json.dumps({"location": [12, 12]}),
    )
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data["status"] == 401
    assert data["error"] == invalid_token_message


def test_edit_a_intervention_location_without_location_data(client):
    response = client.patch(
        "api/v3/interventions/79bb7006-272e-4e0c-8253-117305466b4a/location",
        headers=user1_header,
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == "Please provide valid input data"


def test_edit_a_intervention_location_which_does_not_exist(client):
    response = client.patch(
        "api/v3/interventions/10df0c37-5f2b-4e5d-8b45-7357bbf3bebb/location",
        headers=user1_header,
        data=json.dumps({"location": [12, 12]}),
    )
    assert response.status_code == 404
    data = json.loads(response.data.decode())
    assert data["status"] == 404
    assert (
        data["error"] == "intervention record with specified id does not exist"
    )


def test_edit_a_intervention_location_which_does_not_belong_to_user(client):
    response = client.patch(
        "api/v3/interventions/79bb7006-272e-4e0c-8253-117305466b4a/location",
        headers=user2_header,
        data=json.dumps({"location": [12, 12]}),
    )
    assert response.status_code == 403
    data = json.loads(response.data.decode())
    assert data["status"] == 403
    assert data["error"] == "You are not allowed to modify this resource"


def test_edit_a_intervention_location_with_invalid_intervention_id(client):
    response = client.patch(
        "api/v3/interventions/df/location",
        headers=user2_header,
        data=json.dumps({"location": [12, 12]}),
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == "Invalid incident id"


def test_edit_a_intervention_location_status_of_draft(client):
    response = client.patch(
        "api/v3/interventions/79bb7006-272e-4e0c-8253-117305466b4a/location",
        headers=user1_header,
        data=json.dumps({"location": [12, 12]}),
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["status"] == 200
    assert (
        data["data"][0]["success"] == "Updated intervention record’s location"
    )
    assert data["data"][0]["id"] == "79bb7006-272e-4e0c-8253-117305466b4a"


def test_edit_a_intervention_location_with_invalid_location_coordinates(
    client
):
    response = client.patch(
        "api/v3/interventions/79bb7006-272e-4e0c-8253-117305466b4a/location",
        headers=user1_header,
        data=json.dumps({"location": [-90, 12]}),
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == (
        "latitude must be between -90 and 90 and longitude"
        " coordinates must be between -180 and 180"
    )


def test_edit_a_intervention_location_status_other_than_draft(client):
    response = client.patch(
        "api/v3/interventions/79bb7006-272e-4e0c-8253-117305466b7a/location",
        headers=user1_header,
        data=json.dumps({"location": [12, 12]}),
    )
    assert response.status_code == 403
    data = json.loads(response.data.decode())
    assert data["status"] == 403
    assert data["error"] == "You are not allowed to modify this resource"
