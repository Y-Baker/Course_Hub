#!/usr/bin/python3
"""module to test user nodule"""
import json
import unittest
from flask import Flask
from flask.testing import FlaskClient
from course_hub import auth_views


class UserViewsTestCase(unittest.TestCase):
    def setUp(self):
        # Create a Flask test app
        self.app = Flask(__name__)
        self.app.register_blueprint(auth_views)
        self.client = self.app.test_client()

    def test_sign_up_success(self):
        # Provide valid data for sign up
        data = {
            'email': 'test@example.com',
            'name': 'John Doe',
            'password': 'password123',
            'age': 25
        }

        # Send a POST request to the /api/sign-up endpoint
        response = self.client.post('/api/sign-up', json=data)

        # Check if the response is as expected
        self.assertEqual(response.status_code, 200)
        print(response.get_json())
        self.assertIn('user Created Successfully with id', response.get_json().get("message"))

    def test_sign_up_success_nameNone(self):
        # Provide valid data for sign up
        data = {
            'email': 'test1@example.com',
            'name': None,
            'password': 'password123',
            'age': 25
        }

        # Send a POST request to the /api/sign-up endpoint
        response = self.client.post('/api/sign-up', json=data)

        # Check if the response is as expected
        self.assertEqual(response.status_code, 200)
        print(response.get_json())
        self.assertIn('user Created Successfully with id', response.get_json().get('message'))
    def test_sign_up_invalid_input(self):
        # Provide invalid data for sign up
        data = {
            'email': 'invalid-email',
            'name': '',
            'password': 'short',
            'age': 'abc'
        }

        # Send a POST request to the /api/sign-up endpoint
        response = self.client.post('/api/sign-up', json=data)

        # Check if the response is as expected
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.get_json())


if __name__ == '__main__':
    unittest.main()
