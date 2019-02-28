"""FIle contains model for user"""

from werkzeug.security import generate_password_hash, check_password_hash

from api.utilitiez.responses import (
    duplicate_email,
    duplicate_user_name,
    duplicate_phone_number,
)
from database.db import DatabaseConnection


class User:
    """class defines the user objects structure"""

    def __init__(self, **kwargs):
        # Generating a user's database
        self.db = DatabaseConnection()

    def insert_user(self, **kwargs):
        """User class method for adding new user to the users database"""
        first_name = kwargs["first_name"]
        last_name = kwargs["last_name"]
        other_names = kwargs["other_names"]
        email = kwargs["email"]
        phone_number = kwargs["phone_number"]
        user_name = kwargs.get("user_name")
        user_password = generate_password_hash(kwargs["password"])

        # Querry for adding a new user into users_db
        sql = (
            "INSERT INTO users ("
            "first_name,"
            "last_name, "
            "other_names,"
            "email, phone_number, user_name,"
            "user_password )VALUES ("
            f"'{first_name}', '{last_name}','{other_names}',"
            f"'{email}', '{phone_number}','{user_name}',"
            f"'{user_password}') returning "
            "user_id,first_name as firstname,"
            "last_name as lastname, "
            "other_names as othernames,"
            "email, phone_number as phoneNumber, "
            "user_name as userName, "
            "registered_on as registered"
        )
        self.db.cursor_database.execute(sql)
        new_user = self.db.cursor_database.fetchone()
        return new_user

    def check_if_user_exists(self, user_name, email, phone_number):
        """Making sure that user_name, phone_ number and email are unique"""
        user_exists_sql = (
            "SELECT user_name,email, phone_number from users where "
            f"user_name ='{user_name}' OR email='{email}' OR"
            f" phone_number='{phone_number}';"
        )
        self.db.cursor_database.execute(user_exists_sql)
        user_exists = self.db.cursor_database.fetchone()
        error = {}
        # comparing new user details with db users
        if user_exists and user_exists.get("user_name") == user_name:
            error["username"] = duplicate_user_name

        if user_exists and user_exists.get("email") == email:
            error["email"] = duplicate_email

        if user_exists and user_exists.get("phone_number") == phone_number:
            error["phoneNumber"] = duplicate_phone_number
        return error

    def get_user_details(self, user_id):
        """Function for fetching a known user's details"""
        user_sql = (
            "SELECT user_id, user_name, first_name, last_name, other_names, "
            "email,is_admin FROM users "
            f"WHERE user_id='{user_id}';"
        )
        self.db.cursor_database.execute(user_sql)
        user_details = self.db.cursor_database.fetchone()
        return user_details

    def is_valid_credentials(self, user_name, user_password):
        """Function for verrifying user credentials before login"""
        sql = (
            "SELECT user_id,user_name ,user_password FROM users \
                where user_name="
            f"'{user_name}';"
        )
        self.db.cursor_database.execute(sql)

        user_details = self.db.cursor_database.fetchone()

        if (
                user_details
                and user_details.get("user_name") == user_name
                and check_password_hash(
                user_details.get("user_password"), user_password
        )
        ):
            id = user_details.get("user_id")

            return id
        return None
    