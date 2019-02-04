from flask import json

from api.helpers.responses import (
    wrong_name,
    wrong_password,
    wrong_phone_number,
    duplicate_user_name,
    duplicate_email,
    duplicate_phone_number,
)

mimetype = "application/json"
headers = {"Content-Type": mimetype, "Accept": mimetype}

new_user_data = {
    "firstname": "3",
    "lastname": "Joh7n David",
    "email": "userOnehireporter.com",
    "phoneNumber": "07f73125678",
    "password": "password",
    "username": "ur1",
    "othernames": "t5",
}
data_with_wrong_keys = {
    "firstname": "Joseph",
    "lastname": "Bekalaze",
    "otherames": "",
    "email": "bekeplar@gmail.com",
    "firstname": "Joseph",
    "lastname": "Bekalaze",
    "othernames": "",
    "phoneNumber": "0789057968",
    "username": "bekeplar",
}


def test_register_with_no_data(client):
    response = client.post("api/v1/auth/signup", headers=headers)
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["error"] == "Provide provide valid data to register"


def test_register_with_wrong_key(client):
    response = client.post(
        "api/v1/auth/signup",
        headers=headers,
        data=json.dumps(data_with_wrong_keys),
    )
    assert response.status_code == 422
    data = json.loads(response.data.decode())
    assert data["error"] == "Please provide the correct keys for the data"


#
#
def test_register_with_wrong_invalid_format_data(client):
    response = client.post(
        "api/v1/auth/signup", headers=headers, data=json.dumps(new_user_data)
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["error"]["firstname"] == wrong_name
    assert data["error"]["lastname"] == wrong_name
    assert data["error"]["password"] == wrong_password
    assert data["error"]["phoneNumber"] == wrong_phone_number


def test_register_with_valid_format_data(client):
    new_user_data["firstname"] = "John"
    new_user_data["lastname"] = "David"
    new_user_data["othernames"] = "Mark"
    new_user_data["username"] = "JDMark123"
    new_user_data["email"] = "jdmark@email.com"
    new_user_data["phoneNumber"] = "0772123123"
    new_user_data["password"] = "Password123"

    response = client.post(
        "api/v1/auth/signup", headers=headers, data=json.dumps(new_user_data)
    )
    assert response.status_code == 201
    data = json.loads(response.data.decode())
    assert data["data"][0]["success"] == "Account created Successfully"
    assert "id" in data["data"][0]["user"]
    assert data["data"][0]["user"]["email"] == "jdmark@email.com"


def test_register_user_with_duplicate_data(client):
    response = client.post(
        "api/v1/auth/signup", headers=headers, data=json.dumps(new_user_data)
    )
    assert response.status_code == 409
    data = json.loads(response.data.decode())
    assert data["status"] == 409
    assert data["error"]["username"] == duplicate_user_name
    assert data["error"]["email"] == duplicate_email
    assert data["error"]["phoneNumber"] == duplicate_phone_number
