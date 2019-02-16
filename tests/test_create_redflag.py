import unittest
import json
from flask import Response, json
from api.app import create_app
from database.db import DatabaseConnection
from api.models.user import User
from api.models.incident import Incident


class CreateReadFlagTestCase(unittest.TestCase):

    def setUp(self):
        """initializing method for a unit test"""
        self.app = create_app("Testing")
        self.client = self.app.test_client(self)
        self.user_obj = User()
        self.incident_obj = Incident()
        self.db = DatabaseConnection()
        
        self.user = {
                "firstname": "Bekalaze",
                "lastname": "Joseph",
                "othernames": "Beka",
                "username": "bekeplar",
                "email": "bekeplar@gmail.com",
                "password": "Bekeplar1234",
                "phoneNumber": "0789057968"
                }
        self.user_login = {
            'username': 'bekeplar',
            'password': 'Bekeplar1234'
        }

    def test_create_redflag(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user))
        response = self.client.post('api/v1/auth/login', content_type='application/json', data=json.dumps(self.user_login)
        )
        access_token = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        data = {
                "title": "bribery",
                "location": [60, 120],
                "comment": "These are serious allegations",
                "created_by": 1,
                "type": "redflag"
                }
        res = self.client.post('/api/v1/redflags', content_type="application/json",
            data=json.dumps(data), headers={'Authorization': f'Bearer {access_token}'})
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code,401)
        self.assertEqual(response_data['status'], 401)
        self.assertIsInstance(response_data, dict)

    def test_create_redflag_missing_fields(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user))
        response = self.client.post('api/v1/auth/login', content_type='application/json', data=json.dumps(self.user_login)
        )
        access_token = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        data = {
                "title": "",
                "location": "",
                "comment": "",
                "created_by": "",
                "type": ""
                }
        res = self.client.post('/api/v1/redflags', content_type="application/json",
            data=json.dumps(data), headers={'Authorization': f'Bearer {access_token}'})
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code,401)
        self.assertEqual(response_data['status'], 401)
        self.assertIsInstance(response_data, dict)
    