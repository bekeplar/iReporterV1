"""File for all user authentication code"""
from flask_mail import Message, Mail
import datetime
import jwt
from flask import request, jsonify
from functools import wraps
from os import environ

from api.utilitiez.responses import expired_token_message, invalid_token_message
from database.db import DatabaseConnection

mail = Mail()
secret_key = environ.get("JWT_SECRET_KEY", 'this-is-my-secret')
db = DatabaseConnection()


def encode_token(user_id):
    payload = {
        "userid": user_id,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=6),
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256").decode("utf-8")
    return token


def decode_token(token):
    decoded = jwt.decode(str(token), secret_key, algorithm="HS256")
    return decoded


def extract_token_from_header():
    authorizaton_header = request.headers.get("Authorization")
    if not authorizaton_header or "Bearer" not in authorizaton_header:
        return (
            jsonify({"error": "Bad authorization header", "status": 400}),
            400,
        )
    token = str(authorizaton_header).split(" ")[1]
    return token


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = None
        try:
            extract_token_from_header()
            get_current_identity()
            response = func(*args, **kwargs)

        except jwt.ExpiredSignatureError:
            response = (
                jsonify({"error": expired_token_message, "status": 401}),
                401,
            )
        except jwt.InvalidTokenError:
            response = (
                jsonify({"error": invalid_token_message, "status": 401}),
                401,
            )
        return response

    return wrapper


def get_current_identity():
    user_id = decode_token(extract_token_from_header())["userid"]
    sql = f"select user_id from users where user_id='{user_id}';"
    db.cursor_database.execute(sql)
    results = db.cursor_database.fetchone()
    if results:
        return results["user_id"]


def is_admin_user():
    user_id = get_current_identity()
    sql = f"select is_admin from users where user_id='{user_id}';"
    db.cursor_database.execute(sql)
    is_admin = db.cursor_database.fetchone()
    return is_admin["is_admin"]


def non_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if is_admin_user():
            return (
                jsonify(
                    {
                        "error": "Admin cannot access this resource",
                        "status": 401,
                    }
                ),
                401,
            )
        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_admin_user():
            return (
                jsonify(
                    {
                        "error": "Only Admin can access this resource",
                        "status": 401,
                    }
                ),
                401,
            )
        return func(*args, **kwargs)

    return wrapper

def send_mail(message, receiver, subject='iReporterV1 App', reply_to="keplaxireporter@gmail.com"):
    msg = Message(body=message, subject=subject,
                  recipients=[receiver],
                  reply_to=reply_to)
    mail.send(msg)
    return None
