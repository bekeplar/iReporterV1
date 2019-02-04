from flask import json

from api.helpers.responses import invalid_token_message
from .base import user1_header, user2_header


# EDIT A RED-FLAG RECORD'S COMMENT
def test_edit_a_red_flag_comment_without_a_token(client):
    response = client.patch(
        "api/v1/red-flags/10df0c67-5f2b-4e5d-8b45-7357bbf3bebb/comment"
    )
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data["status"] == 401
    assert data["error"] == invalid_token_message


def test_edit_a_red_flag_comment_with_an_invalid_red_flag_id(client):
    response = client.patch(
        "api/v1/red-flags/f/comment",
        headers=user1_header,
        data=json.dumps({"comment": "Massa placerat duis ultricies lacus."}),
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == "Invalid incident id"


def test_edit_a_red_flag_comment_without_comment_data(client):
    response = client.patch(
        "api/v1/red-flags/10df0c67-5f2b-4e5d-8b45-7357bbf3bebb/comment",
        headers=user1_header,
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == "Please provide valid input data"


def test_edit_a_red_flag_comment_for_a_red_flag_record_which_does_not_exist(
    client
):
    response = client.patch(
        "api/v1/red-flags/79bb7006-272e-4e0c-8253-117305466b4a/comment",
        headers=user1_header,
        data=json.dumps({"comment": "Massa placerat duis ultricies lacus."}),
    )
    assert response.status_code == 404
    data = json.loads(response.data.decode())
    assert data["status"] == 404
    assert data["error"] == "red-flag record with specified id does not exist"


def test_edit_a_red_flag_comment_for_a_red_flag_record_with_without_a_comment(
    client
):
    response = client.patch(
        "api/v1/red-flags/10df0c67-5f2b-4e5d-8b45-7357bbf3bebb/comment",
        headers=user1_header,
        data=json.dumps({"comment": ""}),
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == "Field must contain a minimum of 10 characters"


def test_edit_a_red_flag_comment_created_by_another_user(client):
    response = client.patch(
        "api/v1/red-flags/10df0c67-5f2b-4e5d-8b45-7357bbf3bebb/comment",
        headers=user2_header,
        data=json.dumps({"comment": "I diasgree"}),
    )
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data["status"] == 401
    assert data["error"] == "You can only edit comments created by you"


def test_edit_a_red_flag_comment_created_by_the_current_user(client):
    response = client.patch(
        "api/v1/red-flags/10df0c67-5f2b-4e5d-8b45-7357bbf3bebb/comment",
        headers=user1_header,
        data=json.dumps({"comment": "Proin sagittis nisl rhoncus mattis"}),
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["status"] == 200
    assert data["data"][0]["success"] == "Updated red-flag record’s comment"
    assert data["data"][0]["comment"] == "Proin sagittis nisl rhoncus mattis"


def test_edit_a_red_flag_comment_with_status_other_than_draft(client):
    response = client.patch(
        "api/v1/red-flags/df57bf19-1495-40aa-bbc3-5cc792a8f8f2/comment",
        headers=user1_header,
        data=json.dumps({"comment": "Proin sagittis nisl rhoncus mattis "}),
    )
    assert response.status_code == 403
    data = json.loads(response.data.decode())
    assert data["status"] == 403
    error_message = "You cannot edit a record which is Resolved"
    assert data["error"] == error_message


# EDIT A intervention RECORD'S COMMENT
def test_edit_a_intervention_comment_without_a_token(client):
    response = client.patch(
        "api/v1/interventions/79bb7006-272e-4e0c-8253-117305466r4a/comment"
    )
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data["status"] == 401
    assert data["error"] == invalid_token_message


def test_edit_a_intervention_comment_with_an_invalid_intervention_id(client):
    response = client.patch(
        "api/v1/interventions/f/comment",
        headers=user1_header,
        data=json.dumps({"comment": "Massa placerat duis ultricies lacus."}),
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == "Invalid incident id"


def test_edit_a_intervention_comment_without_comment_data(client):
    response = client.patch(
        "api/v1/interventions/79cc7006-272e-4e0c-8253-117305466b4a/comment",
        headers=user1_header,
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == "Please provide valid input data"


def test_edit_a_intervention_comment_for_a_intervention_record_which_does_not_exist(
    client
):
    response = client.patch(
        "api/v1/interventions/79cc7006-272e-4e0c-8253-117302466b4a/comment",
        headers=user1_header,
        data=json.dumps({"comment": "Massa placerat duis ultricies lacus."}),
    )
    assert response.status_code == 404
    data = json.loads(response.data.decode())
    assert data["status"] == 404
    assert (
        data["error"] == "intervention record with specified id does not exist"
    )


def test_edit_a_intervention_comment_for_a_intervention_record_with_without_a_comment(
    client
):
    response = client.patch(
        "api/v1/interventions/79cc7006-272e-4e0c-8253-117305466b4a/comment",
        headers=user1_header,
        data=json.dumps({"comment": ""}),
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == "Field must contain a minimum of 10 characters"


def test_edit_a_intervention_comment_created_by_another_user(client):
    response = client.patch(
        "api/v1/interventions/79cc7006-272e-4e0c-8253-117305466b4a/comment",
        headers=user2_header,
        data=json.dumps({"comment": "I diasgree"}),
    )
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data["status"] == 401
    assert data["error"] == "You can only edit comments created by you"


def test_edit_a_intervention_comment_created_by_the_current_user(client):
    response = client.patch(
        "api/v1/interventions/79cc7006-272e-4e0c-8253-117305466b4a/comment",
        headers=user1_header,
        data=json.dumps({"comment": "Proin sagittis nisl rhoncus mattis"}),
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["status"] == 200
    assert (
        data["data"][0]["success"] == "Updated intervention record’s comment"
    )
    assert data["data"][0]["comment"] == "Proin sagittis nisl rhoncus mattis"


def test_edit_a_intervention_comment_with_status_other_than_draft(client):
    response = client.patch(
        "api/v1/interventions/79cc7006-224e-4e0c-8253-117305466b4a/comment",
        headers=user1_header,
        data=json.dumps({"comment": "Proin sagittis nisl rhoncus mattis "}),
    )
    assert response.status_code == 403
    data = json.loads(response.data.decode())
    assert data["status"] == 403
    error_message = "You cannot edit a record which is Resolved"
    assert data["error"] == error_message
