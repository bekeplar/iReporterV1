"""Module contains functions for validating user inputs as provided"""
import re
from flask import jsonify, request, abort
from functools import wraps
from uuid import UUID

from api.helpers.responses import (
    wrong_password,
    wrong_username,
    wrong_email,
    wrong_phone_number,
    wrong_name,
)


def request_data_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not request.data:
            return (
                jsonify(
                    {"error": "Please provide valid input data", "status": 400}
                ),
                400,
            )
        return func(*args, **kwargs)

    return wrapper


def sign_up_data_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = None
        if not request.data:

            response = (
                jsonify(
                    {
                        "error": "Provide provide valid data to register",
                        "status": 400,
                    }
                ),
                400,
            )
        else:
            response = func(*args, **kwargs)
        return response

    return wrapper


def is_number(num_value):
    """Checks if num_value is a number"""
    if isinstance(num_value, int) or isinstance(num_value, float):
        return True
    return False


def is_string(str_value):
    """Checks if input is a string"""
    if (
            str_value
            and isinstance(str_value, str)
            and not str(str_value).isspace()
            and not str_value.isnumeric()
    ):
        return True
    return False


def contains_space(str_value):
    """Checks if input contains a space"""
    if " " in str_value or len(str(str_value).split(" ")) > 1:
        return True
    return False


def contains_number(str_value):
    """Checks if input contains a space"""
    for character in str_value:
        if character.isdigit():
            return True
    return False


def validate_email(email):
    if not email or not re.match("[^@]+@[^@]+\.[^@]+", email):
        return wrong_email
    return None


def validate_user_name(user_name):
    if user_name and not is_number(user_name) and len(user_name) >= 5:
        return None
    return wrong_username


def validate_name(name, required=1):
    error = wrong_name
    if not required and len(str(name).strip()) == 0:
        error = None
    elif (
            name
            and is_string(name)
            and not contains_space(name)
            and not contains_number(name)
    ):
        error = None
    return error


def validate_password(password):
    error = wrong_password
    if (
            len(password) >= 8
            and re.search("[A-Z]", password)
            and re.search("[0-9]", password)
            and re.search("[a-z]", password)
    ):
        error = None
    return error


def validate_phone_number(phone_number):
    error = wrong_phone_number

    if len(phone_number) == 10 and phone_number.isdigit():
        error = None
    return error


def validate_new_user(**kwargs):
    errors = dict()
    errors["firstname"] = validate_name(kwargs["first_name"])
    errors["lastname"] = validate_name(kwargs["last_name"])
    errors["othernames"] = validate_name(kwargs["other_names"], 0)
    errors["username"] = validate_user_name(kwargs["user_name"])
    errors["password"] = validate_password(kwargs["password"])
    errors["email"] = validate_email(kwargs["email"])
    errors["phoneNumber"] = validate_phone_number(kwargs["phone_number"])
    invalid_fields = {key: value for key, value in errors.items() if value}
    if invalid_fields:
        return jsonify({"status": 400, "error": invalid_fields}), 400
    return None


def validate_sentence(sentence, min_len=0, max_len=0):
    error = None
    sentence = str(sentence).strip()
    if sentence.isdigit():
        error = "Field cannot be a number"
    elif len(sentence) < min_len:
        error = f"Field must contain a minimum of {str(min_len)} characters"
    elif max_len and len(sentence) > max_len:
        error = f"Field must contain a maximum of {str(max_len)} characters"

    return error


media_format = {"Videos": [".mp4", "MP4"], "Images": ["jpg", "JPEG"]}


def is_validate_media_type(collection, media_type):
    for media in collection:
        if not media.endswith(media_format.get(media_type)[0]):
            return False
    return True


def validate_media(media_collection, media_type):
    media_format = {"Videos": [".mp4", "MP4"], "Images": ["jpg", "JPEG"]}
    error = None
    if not isinstance(media_collection, list):
        error = f"Please provide an empty list of {media_type} if none"
    elif not is_validate_media_type(media_collection, media_type):
        error = (
            f"Only {media_format.get(media_type)[1]} {media_type} are "
            "supported"
        )

    return error


def validate_location(location):
    error = None
    if not isinstance(location, list) or not len(location) == 2:
        error = (
            "location must be a list with both Latitude and Longitude "
            "coordinates"
        )
    elif not is_number(location[0]) or not is_number(location[1]):
        error = "location coordinates must be a number"
    elif not -90 < location[0] < 90 or not -180 < location[1] < 180:
        error = (
            "latitude must be between -90 and 90 and longitude "
            "coordinates must be between -180 and 180"
        )

    return error


def validate_new_incident(**kwargs):
    errors = dict()
    errors["title"] = validate_sentence(kwargs.get("title"), 4, 100)
    errors["comment"] = validate_sentence(kwargs.get("comment"), 10)
    errors["location"] = validate_location(kwargs.get("location"))
    errors["Images"] = validate_media(kwargs.get("images"), "Images")
    errors["Videos"] = validate_media(kwargs.get("videos"), "Videos")
    errors["type"] = validate_type(kwargs.get("inc_type"))
    not_valid = {key: value for key, value in errors.items() if value}

    if not_valid:
        return (jsonify({"status": 400, "error": not_valid}), 400)
    return None


# def is_valid_uuid(func):
#     @wraps(func)
#     def decorated_view(*args, **kwargs):
#         value = kwargs["incident_id"]

#         try:
#             value = UUID(value, version=4)
#         except ValueError:
#             return (
#                 jsonify({"status": 400, "error": "Invalid incident id"}),
#                 400,
#             )
#         return func(*args, **kwargs)

#     return decorated_view


def validate_edit_location(location):
    error = validate_location(location)
    if error:
        return error
    else:
        return None


def is_valid_status(status):
    is_valid = True
    if not status or not isinstance(status, str):
        is_valid = False
    elif str(status).lower() not in (
            "draft",
            "resolved",
            "under investigation",
            "rejected",
    ):
        is_valid = False
    return is_valid


def validate_type(inc_type):
    if inc_type == "red-flag" or inc_type == "intervention":
        return None
    else:
        return "type must either be red-flag or intervention"


# def parse_incident_type(func):
#     @wraps(func)
#     def decorated_view(*args, **kwargs):
#         incident_type = kwargs["incidents"]

#         if incident_type == "red-flags" or incident_type == "interventions":
#             return func(*args, **kwargs)
#         abort(404)

#     return decorated_view
