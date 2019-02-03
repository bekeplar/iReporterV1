import datetime

# from api.models.incident import Incident
from jwt import encode

from api.helpers.auth_token import encode_token, secret_key
from database.db import DatabaseConnection

db = DatabaseConnection()


def get_user_id(user_name):
    sql = f"SELECT id FROM users WHERE user_name='{user_name}'"
    db.cursor.execute(sql)
    result = db.cursor.fetchone()
    return result.get("id")


def generate_token_header(token):
    return {
        "Content-Type": "application/json",
        "Authorization": str("Bearer " + token),
    }


admin_id = get_user_id("admin")
admin_header = generate_token_header(encode_token(admin_id))

user1_id = get_user_id("user1")
user2_id = get_user_id("user2")

user1_header = generate_token_header(encode_token(user1_id))
user2_header = generate_token_header(encode_token(user2_id))

new_red_flag = {
    "title": "My First red flag",
    "comment": "Lorem ipsum eiusmod temport labore et dolore magna",
    "location": [-80, -174.4],
    "Images": ["image1.jpg", "image2.jpg"],
    "Videos": ["vid1.mp4", "vid2.mp4"],
    "type": "red-flag",
}

new_intervention = {
    "title": "Broken bridge",
    "comment": (
        "Mi proin sed libero enim sed faucibus turpis in."
        "Adipiscing bibendum est ultricies integer quis auctor elit"
    ),
    "location": [-72, -154.4],
    "Images": ["image6.jpg", "image7.jpg"],
    "Videos": ["vid8.mp4", "vid5.mp4"],
    "type": "intervention",
}

expired_token = encode(
    {
        "userid": user1_id,
        "exp": datetime.datetime.utcnow() - datetime.timedelta(hours=3),
    },
    secret_key,
    algorithm="HS256",
).decode("utf-8")
expired_token_header = generate_token_header(expired_token)

invalid_id_token = encode(
    {
        "userid": "58841703-eeab-46d2-ab3b-dcf93bf436c7",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1),
    },
    secret_key,
    algorithm="HS256",
).decode("utf-8")

invalid_id_token_header = generate_token_header(invalid_id_token)
