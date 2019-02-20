import unittest
import datetime
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
        self.incident_obj = Incident()
        self.db = DatabaseConnection()
        self.user_data = {
                "firstname": "Bekalaze",
                "lastname": "Joseph",
                "othernames": "Beka",
                "username": "bekeplar",
                "email": "bekeplar@gmail.com",
                "password": "Bekeplar1234",
                "phoneNumber": "0772787777"
                }
            
        self.user_login_data = {
                       "username":"bekeplar",
                       "password": "Bekeplar1234"
                     }

        self.redflag_data = {
                "title": "bribery",
                "location": [60, 120],
                "comment": "These are serious allegations",
                "created_by": 1,
                "type": "redflag"
                }

        self.redflag1_data = {
                "title": "",
                "location": "",
                "comment": "",
                "created_by": "",
                "type": ""
                }
        
        self.intervention_data = {
                "title": "bribery",
                "location": [60, 120],
                "comment": "These are serious allegations",
                "created_by": 1,
                "type": "intervention"
                }
        self.intervention1_data = {
                "title": "",
                "location": "",
                "comment": "",
                "created_by": "",
                "type": ""
                }

    
    def test_home_page(self):
        """unit test for success to index endpoint"""
        response = self.client.get("/", content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data).get("message"), "Welcome to iReporter Api V1")

    def test_method_not_allowed(self):
        """unit test for method not allowed error"""
        response = self.client.patch('/', data=json.dumps({
            "username": "username",
            "password": "password"
        }), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response_data.get("error"), "Method not allowed")

    def test_page_not_found(self):
        """unit test for page not found error"""
        response = self.client.get(
            "url/not/exist", content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data.get("error"), "Endpoint for specified URL does not exist")

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

    def test_create_redflag_without_data(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        access_token = json.loads(res1.data.decode())
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v1/redflags', content_type="application/json",
            headers={'Authorization': 'Bearer ' + str(access_token)}, data=json.dumps(self.redflag1_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)
        self.assertEqual(response_data['status'], 401)
        self.assertIsInstance(response_data, dict)


    def test_create_redflag_with_no_token(self):
       
        res = self.client.post('/api/v1/redflags', content_type="application/json",
            data=json.dumps(self.redflag_data))
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

    def test_create_new_intervention_missing_data(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        access_token = json.loads(res1.data.decode())
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v1/interventions', content_type="application/json",
            headers={'Authorization': 'Bearer ' + str(access_token)}, data=json.dumps(self.intervention1_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)
        self.assertEqual(response_data['status'], 401)
        self.assertIsInstance(response_data, dict)


    def test_create_new_intervention_twice(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        access_token = json.loads(res1.data.decode())
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/interventions', content_type="application/json",
            headers={'Authorization': 'Bearer ' + str(access_token)}, data=json.dumps(self.intervention_data))
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

    def test_get_all_created_intervention(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        access_token = json.loads(res1.data.decode())
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/interventions', content_type="application/json",
            headers={'Authorization': 'Bearer ' + str(access_token)}, data=json.dumps(self.intervention_data))
        res = self.client.get('/api/v1/interventions', content_type="application/json",
            headers={'Authorization': 'Bearer ' + str(access_token)}, data=json.dumps(self.intervention_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)
        self.assertEqual(response_data['status'], 401)
        self.assertIsInstance(response_data, dict)

    def test_get_all_redflags(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        access_token = json.loads(res1.data.decode())
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/redflags', content_type="application/json",
            headers={'Authorization': 'Bearer ' + str(access_token)}, data=json.dumps(self.redflag_data))
        res = self.client.get('/api/v1/redflags', content_type="application/json",
            headers={'Authorization': 'Bearer ' + str(access_token)}, data=json.dumps(self.redflag_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)
        self.assertEqual(response_data['status'], 401)
        self.assertIsInstance(response_data, dict)

    def test_get_one_redflag_record(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        access_token = json.loads(res1.data.decode())
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/redflags', content_type="application/json",
            headers={'Authorization': 'Bearer ' + str(access_token)}, data=json.dumps(self.redflag_data))
        res = self.client.get('/api/v1/redflags/1', content_type="application/json",
            headers={'Authorization': 'Bearer ' + str(access_token)}, data=json.dumps(self.redflag_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)
        self.assertEqual(response_data['status'], 401)
        self.assertIsInstance(response_data, dict)

    def test_delete_redflag_record(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        access_token = json.loads(res1.data.decode())
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/redflags', content_type="application/json",
            headers={'Authorization': 'Bearer ' + str(access_token)}, data=json.dumps(self.redflag_data))
        res = self.client.delete('/api/v1/redflags/1', content_type="application/json",
            headers={'Authorization': 'Bearer ' + str(access_token)}, data=json.dumps(self.redflag_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)
        self.assertEqual(response_data['status'], 401)
        self.assertIsInstance(response_data, dict)

    def test_delete_created_intervention(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        access_token = json.loads(res1.data.decode())
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/interventions', content_type="application/json",
            headers={'Authorization': 'Bearer ' + str(access_token)}, data=json.dumps(self.intervention_data))
        res = self.client.delete('/api/v1/interventions/1', content_type="application/json",
            headers={'Authorization': 'Bearer ' + str(access_token)}, data=json.dumps(self.intervention_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)
        self.assertEqual(response_data['status'], 401)
        self.assertIsInstance(response_data, dict)

    def tearDown(self):
            self.db.drop_table('users')
            self.db.drop_table('incidents')
    


