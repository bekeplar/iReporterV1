from flask import json

from api.helpers.responses import invalid_token_message
from .base import (
    admin_header,
    user1_header,
    new_red_flag,
    user1_id,
    user2_id,
    user2_header,
    new_intervention,
    invalid_id_token_header,
)


# # CREATE A RED-FLAG
def test_create_a_red_flag_without_a_token(client):
    # test only logged in user with token
    response = client.post("api/v3/incidents")
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data == {"error": invalid_token_message, "status": 401}


def test_create_a_red_flag_with_invalid_token(client):
    # test onlcreate incident record with invalid token
    response = client.post("api/v3/incidents", headers=invalid_id_token_header)
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data == {
        "error": "You are not authorized to access this resource",
        "status": 401,
    }


def test_create_a_red_flag_with_bad_json_format_data(client):
    response = client.post(
        "/api/v3/incidents", headers=user1_header, data="my incident"
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["error"] == "Bad JSON format data"


def test_admin_cannot_create_a_red_flag(client):
    response = client.post(
        "api/v3/incidents", headers=admin_header, data=json.dumps(new_red_flag)
    )
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data == {
        "error": "Admin cannot access this resource",
        "status": 401,
    }


def test_create_a_red_flag_without_data(client):
    response = client.post("api/v3/incidents", headers=user1_header)
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["error"] == "Please provide incident Data"


def test_create_a_red_flag_with_valid_data(client):
    new_red_flag[
        "comment"
    ] = "Lorem ipsum eiusmod temport labore et dolore magna"
    response = client.post(
        "api/v3/incidents", headers=user1_header, data=json.dumps(new_red_flag)
    )
    assert response.status_code == 201
    data = json.loads(response.data.decode())
    assert data["data"][0]["success"] == "Created red-flag record"
    assert data["data"][0]["red-flag"]["created_by"] == user1_id


def test_create_a_red_flag_without_wrong_input(client):
    wrong_input_1 = new_red_flag

    new_red_flag["location"] = ["jk", 180]
    response = client.post(
        "api/v3/incidents", headers=user1_header, data=json.dumps(new_red_flag)
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["error"]["location"] == "location coordinates must be a number"
    assert len(data["error"]) == 1

    wrong_input_1["title"] = "6"
    wrong_input_1["location"] = ""
    wrong_input_1["tags"] = ""
    wrong_input_1["Images"] = ""
    wrong_input_1["Videos"] = ""
    wrong_input_1["comment"] = "5"

    # create a red flag with one coordinate in the location
    response = client.post(
        "api/v3/incidents",
        headers=user1_header,
        data=json.dumps(wrong_input_1),
    )

    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["error"]["title"] == "Field cannot be a number"
    assert (
        data["error"]["location"]
        == "location must be a list with both Latitude and Longitude coordinates"
    )

    assert (
        data["error"]["Images"]
        == "Please provide an empty list of Images if none"
    )
    assert (
        data["error"]["Videos"]
        == "Please provide an empty list of Videos if none"
    )
    assert data["error"]["comment"] == "Field cannot be a number"
    assert len(data["error"]) == 5

    wrong_input_1["title"] = "my"
    wrong_input_1["location"] = [-90, 180]
    wrong_input_1["tags"] = [12]
    wrong_input_1["Images"] = ["mine.png"]
    wrong_input_1["Videos"] = ["crime.mpeg"]
    wrong_input_1["comment"] = "Lorem ipsum"

    response = client.post(
        "api/v3/incidents",
        headers=user1_header,
        data=json.dumps(wrong_input_1),
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert (
        data["error"]["title"]
        == "Field must contain a minimum of 4 characters"
    )
    assert (
        data["error"]["location"]
        == "latitude must be between -90 and 90 and longitude coordinates must be between -180 and 180"
    )

    assert data["error"]["Images"] == "Only JPEG Images are supported"
    assert data["error"]["Videos"] == "Only MP4 Videos are supported"
    assert len(data["error"]) == 4

    wrong_input_1["title"] = ""

    response = client.post(
        "api/v3/incidents",
        headers=user1_header,
        data=json.dumps(wrong_input_1),
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert (
        data["error"]["title"]
        == "Field must contain a minimum of 4 characters"
    )

    wrong_input_1["title"] = (
        "orem ipsum dolor sit amet, consectetur adipiscing elit. Mauris sit amet massa"
        " in elit accumsan bibendum. Suspendisse tincidunt, justo quis laoreet elementum,"
        "enim ligula consectetur ligula, quis fringilla ligula augue non nibh. "
    )
    wrong_input_1["type"] = "redflag"

    response = client.post(
        "api/v3/incidents",
        headers=user1_header,
        data=json.dumps(wrong_input_1),
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert (
        data["error"]["title"]
        == "Field must contain a maximum of 100 characters"
    )


def test_create_an_intervention_with_valid_data(client):
    response = client.post(
        "api/v3/incidents",
        headers=user2_header,
        data=json.dumps(new_intervention),
    )
    assert response.status_code == 201
    data = json.loads(response.data.decode())
    assert data["data"][0]["success"] == "Created intervention record"
    assert data["data"][0]["intervention"]["created_by"] == user2_id
    assert data["data"][0]["intervention"]["comment"] == (
        "Mi proin sed libero enim sed faucibus turpis in."
        "Adipiscing bibendum est ultricies integer quis auctor elit"
    )

    assert data["data"][0]["intervention"]["title"] == ("Broken bridge")
