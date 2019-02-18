import unittest
import json
from flask import Response, json
from api.app import create_app
from database.db import DatabaseConnection
from api.models.user import User
from api.models.incident import Incident


class IncidentTestCase(unittest.TestCase):

    def setUp(self):
        """initializing method for a unit test"""
        self.app = create_app("Testing")
        self.client = self.app.test_client(self)
        self.user_obj = User()
        self.db = DatabaseConnection()
        self.user_data = {
                "firstname": "Bekalaze",
                "lastname": "Joseph",
                "othernames": "Beka",
                "username": "bekeplax",
                "email": "bekeplax@gmail.com",
                "password": "Bekeplar1234",
                "phoneNumber": "0772787777"
                }
            
        self.user_login_data = {
                       "username":"bekeplax",
                       "password": "Bekeplar1234"
                     }

        self.redflag_data = {
                "title": "bribery",
                "location": [60, 120],
                "comment": "These are serious allegations",
                "created_by": 1,
                "type": "redflag"
                }
        
        self.intervention_data = {
                "title": "bribery",
                "location": [60, 120],
                "comment": "These are serious allegations",
                "created_by": 1,
                "type": "intervention"
                }
    def tearDown(self):
            self.db.drop_table('users')
            self.db.drop_table('incidents')

    def test_create_redflag(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        access_token = json.loads(res1.data.decode())
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v1/redflags', content_type="application/json",
            headers={'Authorization': 'Bearer ' + str(access_token)}, data=json.dumps(self.redflag_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)
        self.assertEqual(response_data['status'], 401)
        self.assertIsInstance(response_data, dict)

    def test_create_new_intervention(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        access_token = json.loads(res1.data.decode())
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v1/interventions', content_type="application/json",
            headers={'Authorization': 'Bearer ' + str(access_token)}, data=json.dumps(self.intervention_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)
        self.assertEqual(response_data['status'], 401)
        self.assertIsInstance(response_data, dict)

    def test_get_created_intervention(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        access_token = json.loads(res1.data.decode())
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/interventions', content_type="application/json",
            headers={'Authorization': 'Bearer ' + str(access_token)}, data=json.dumps(self.intervention_data))
        res = self.client.get('/api/v1/interventions/1', content_type="application/json",
            headers={'Authorization': 'Bearer ' + str(access_token)}, data=json.dumps(self.intervention_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)
        self.assertEqual(response_data['status'], 401)
        self.assertIsInstance(response_data, dict)

