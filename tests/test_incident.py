import unittest
import json
from api.app import create_app
from database.db import DatabaseConnection
from api.utilitiez.auth_token import encode_token
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
        
        self.user_id = 1
        self.token = encode_token(self.user_id)

        
        
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

        self.data = {}

        self.new_comment = {
            "comment": "People change if tasked to" 
        }

        self.new_status = {
            "status": "resolved" 
        }

        self.new_location = {
            "location": [45, 115] 
        }

    def tearDown(self):
            self.db.drop_table('users')
            self.db.drop_table('incidents')

    
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

    def test_not_authorised(self):
        """unit test for method not allowed error"""
        response = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps({
            "username": "username",
            "password": "password"
        }))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("error"), "Wrong login credentials.")

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
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v1/redflags', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.redflag_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 201)
        self.assertEqual(response_data['status'], 201)
        self.assertIsInstance(response_data, dict)

    def test_create_redflag_without_data(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v1/redflags', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token})
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(response_data['status'], 400)
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
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v1/interventions', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.intervention_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 201)
        self.assertEqual(response_data['status'], 201)
        self.assertIsInstance(response_data, dict)

    def test_duplicate_redflag(self):
            self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
            res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
            self.assertEqual(res1.status_code, 200)
            self.client.post('/api/v1/redflags', content_type="application/json",
                headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.redflag_data))
            res = self.client.post('/api/v1/redflags', content_type="application/json",
                headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.redflag_data))
            response_data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 409)
            self.assertEqual(response_data['status'], 409)
            self.assertIsInstance(response_data, dict)


    def test_create_new_intervention_missing_data(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        
        res = self.client.post('/api/v1/interventions', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token})
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)


    def test_create_new_intervention_twice(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/interventions', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.intervention_data))
        res = self.client.post('/api/v1/interventions', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.intervention_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 409)
        self.assertEqual(response_data['status'], 409)
        self.assertIsInstance(response_data, dict)

    def test_get_created_intervention(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/interventions', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.intervention_data))
        res = self.client.get('/api/v1/interventions/1', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.intervention_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data['status'], 200)
        self.assertIsInstance(response_data, dict)

    def test_get_all_created_intervention(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/interventions', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.intervention_data))
        res = self.client.get('/api/v1/interventions', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.intervention_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data['status'], 200)
        self.assertIsInstance(response_data, dict)

    def test_get_all_intervention_empty_database(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.get('/api/v1/interventions', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.intervention_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data['status'], 200)
        self.assertIsInstance(response_data, dict)


    def test_get_all_redflags(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/redflags', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.redflag_data))
        res = self.client.get('/api/v1/redflags', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.redflag_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data['status'], 200)
        self.assertIsInstance(response_data, dict)

    def test_get_all_redflags_from_empty_database(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.get('/api/v1/redflags', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.redflag_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data['status'], 200)
        self.assertIsInstance(response_data, dict)

    def test_get_one_redflag_record(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/redflags', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.redflag_data))
        res = self.client.get('/api/v1/redflags/1', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.redflag_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data['status'], 200)
        self.assertIsInstance(response_data, dict)

    def test_delete_redflag_record(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/redflags', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.redflag_data))
        res = self.client.delete('/api/v1/redflags/1', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.redflag_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data['status'], 200)
        self.assertIsInstance(response_data, dict)

    def test_delete_non_existing_redflag_record(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/redflags', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.redflag_data))
        res = self.client.delete('/api/v1/redflags/3', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.redflag_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 404)
        self.assertEqual(response_data['status'], 404)
        self.assertIsInstance(response_data, dict)


    def test_delete_created_intervention(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/interventions', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.intervention_data))
        res = self.client.delete('/api/v1/interventions/1', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.intervention_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data['status'], 200)
        self.assertIsInstance(response_data, dict)

    def test_delete_intervention_not_in_database(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/interventions', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.intervention_data))
        res = self.client.delete('/api/v1/interventions/2', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.intervention_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 404)
        self.assertEqual(response_data['status'], 404)
        self.assertIsInstance(response_data, dict)


    def test_edit_intervention_comment(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/interventions', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.intervention_data))
        res = self.client.patch('/api/v1/interventions/1/comment', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.new_comment))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data['status'], 200)
        self.assertIsInstance(response_data, dict)


    def test_edit_redflag_comment(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/redflags', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.redflag_data))
        res = self.client.patch('/api/v1/redflags/1/comment', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.new_comment))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data['status'], 200)
        self.assertIsInstance(response_data, dict)

    def test_edit_intervention_location(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/interventions', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.intervention_data))
        res = self.client.patch('/api/v1/interventions/1/location', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.new_location))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data['status'], 200)
        self.assertIsInstance(response_data, dict)


    def test_edit_redflag_location(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/redflags', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.redflag_data))
        res = self.client.patch('/api/v1/redflags/1/location', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.new_location))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data['status'], 200)
        self.assertIsInstance(response_data, dict)

    def test_edit_redflag_location_no_token(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/redflags', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.redflag_data))
        res = self.client.patch('/api/v1/redflags/1/location', content_type="application/json",
            data=json.dumps(self.new_location))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)
        self.assertEqual(response_data['status'], 401)
        self.assertIsInstance(response_data, dict)

    def test_edit_intervention_status_not_admin(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/interventions', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.intervention_data))
        res = self.client.patch('/api/v1/interventions/1/status', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.new_status))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)
        self.assertEqual(response_data['status'], 401)
        self.assertIsInstance(response_data, dict)


    def test_edit_redflag_status_not_admin(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/redflags', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.intervention_data))
        res = self.client.patch('/api/v1/redflags/1/status', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.new_status))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)
        self.assertEqual(response_data['status'], 401)
        self.assertIsInstance(response_data, dict)


    
    




