from flask import Response, json
from api.app import create_app
from database.db import DatabaseConnection
from api.models.user import User
from werkzeug.security import generate_password_hash
import unittest
import datetime
from api.helpers.auth_token import (
    token_required,
    non_admin,
    admin_required,
    get_current_identity,
)

class BaseTest(unittest.TestCase):
    def setUp(self):
        """initializing method for a unit test"""
        self.app = create_app("Testing")
        self.client = self.app.test_client(self)
        self.user_obj = User()
        self.db = DatabaseConnection()

    
    def get_token_admin(self):
        admin_data_login = {
            "email": "ken@gmail.com",
            "password": "Ken1234567"
        }
        res = self.client.post('/api/v1/auth/login', content_type="application/json",
                            data=json.dumps(admin_data_login))
        data = json.loads(res.data.decode())
        return data['access_token']

    def get_token_user(self):
        user_data = {
            "firstname": "len",
            "lastname": "leno",
            "othernames": "ken",
            "email": "len@gmail.com",
            "phonenumber": 256786578719,
            "username": "len",
            "password": "1awQdddddd"
        }
        user_data_login = {
            "email": "len@gmail.com",
            "password": "1awQdddddd"
        }
        self.client.post('/api/v1/auth/signup', content_type="application/json",
                      data=json.dumps(user_data))
        res = self.client.post('/api/v1/auth/login', content_type="application/json",
                            data=json.dumps(user_data_login))
        data = json.loads(res.data.decode())
        return data

    def user_header(self):
        return {'content_type': "application/json", 'Authorization':"Bearer + token"}

    def admin_header(self):
        return {'content_type': "application/json", 'Authorization':"Bearer + token"}

    # def create_admin(self):
    #     return self.user_obj.insert_user("Bekalaze","Joseph", "Beka","bekeplar@gmail.com","0789057968","bekeplar", generate_password_hash(
    #                                 "Bekeplar1234"),
    #                             datetime.datetime.now(), isAdmin=True)


    def tearDown(self):
        self.db.drop_table('users')
