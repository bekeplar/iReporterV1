# import unittest

# from flask import json

# from database.db import DatabaseConnection
# from api.models.incident import Incident
# from api.models.incident import Incident
# from api.models.user import User
# from tests.base_test import BaseTest

# from api.app import create_app

# class RedflagTestCase(BaseTest):
#     def test_returns_error_if_the_record_type_is_empty(self):
#         data = {
#                 "incident_type":"",
#                 "location":[3333.33, 444.1],
#                 "comment": "its terrible",
#                 }
#         res = self.client.post('/api/v1/redflags', content_type="application/json",
#             data=json.dumps(data), headers = self.user_header())
#         response_data = json.loads(res.data.decode())
#         self.assertEqual(res.status_code,400)
#         self.assertEqual(response_data['status'], 400)
#         self.assertIsInstance(response_data, dict)
#         self.assertEqual(response_data['error'], "A required field is either missing or empty")

#     def test_returns_error_if_the_record_type_is_invalid(self):
#         data = {
#                 "incident_type":"red",
#                 "location":[3333.33, 444.1],
#                 "comment": "its terrible",
#                 }
#         res = self.client.post('/api/v1/redflags', content_type="application/json",
#             data=json.dumps(data), headers = self.user_header())
#         response_data = json.loads(res.data.decode())
#         self.assertEqual(res.status_code,400)
#         self.assertEqual(response_data['status'], 400)
#         self.assertIsInstance(response_data, dict)
#         self.assertEqual(response_data['error'], "type must a string and must be red-flag or intervention")
        
#     def test_returns_error_if_the_record_type_is_not_a_string(self):
#         data = {
#                 "incident_type":9,
#                 "location":[3333.33, 444.1],
#                 "comment": "its terrible",
#                 }
#         res = self.client.post('/api/v1/redflags', content_type="application/json",
#             data=json.dumps(data), headers = self.user_header())
#         response_data = json.loads(res.data.decode())
#         self.assertEqual(res.status_code,400)
#         self.assertEqual(response_data['status'], 400)
#         self.assertIsInstance(response_data, dict)
#         self.assertEqual(response_data['error'], "type must a string and must be red-flag or intervention")

#     def test_return_error_if_location_is_invalid(self):
#         data = {
#                 "incident_type":"red-flag",
#                 "location":"2222222",
#                 "comment": "its terrible",
#                 } 
#         res = self.client.post('/api/v1/redflags', content_type="application/json",
#             data=json.dumps(data), headers = self.user_header())
#         response_data = json.loads(res.data.decode())
#         self.assertEqual(res.status_code,400)
#         self.assertEqual(response_data['status'], 400)
#         self.assertIsInstance(response_data, dict)
#         self.assertEqual(response_data['error'],"Location field only takes in a list of valid Lat and Long cordinates")

#     def test_returns_error_if_comment_is_not_valid(self):
#         data = {
#                 "incident_type":"red-flag",
#                 "location":[3333.33, 444.1],
#                 "comment": 99,
#                 }
#         res = self.client.post('/api/v1/redflags', content_type="application/json",
#             data=json.dumps(data), headers = self.user_header())
#         response_data = json.loads(res.data.decode())
#         self.assertEqual(res.status_code,400)
#         self.assertEqual(response_data['status'], 400)
#         self.assertIsInstance(response_data, dict)
#         self.assertEqual(response_data['error'], "comment must be a string")

#     def test_returns_error_if_unauthorised_user_tries_to_post_record(self):
#         data = {
#             "incident_type":"red-flag",
#             "location":[3333.33, 444.1],
#             "comment": "the pot holes are many",
#             }
#         res = self.client.post('/api/v1/redflags', content_type="application/json",
#             data=json.dumps(data), headers = self.admin_header())
#         response_data = json.loads(res.data.decode())
#         self.assertEqual(res.status_code,403)
#         self.assertEqual(response_data['status'], 403)
#         self.assertIsInstance(response_data, dict)
#         self.assertEqual(response_data['error'], "You do not have permission to perform this action")

#     def test_posts_incident_record(self):
#         data = {
#             "incident_type":"red-flag",
#             "location":[3333.33, 444.1],
#             "comment": "the pot holes are many",
#             }
#         res = self.client.post('/api/v1/redflags', content_type="application/json",
#             data=json.dumps(data), headers = self.user_header())
#         response_data = json.loads(res.data.decode())
#         self.assertEqual(res.status_code, 201)
#         self.assertEqual(response_data['status'], 201)
#         self.assertIsInstance(response_data, dict)
#         self.assertIn("the pot holes are many", str(response_data['data']))
#         self.assertEqual(response_data['message'], "created red-flag record successfuly")
