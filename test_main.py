'''
Tests for jwt flask app.
'''
import os
import json
import pytest
import unittest
import main
import datetime

from flask import Flask
from main import APP
from unittest.mock import patch, MagicMock

app = Flask(__name__)

SECRET = 'TestSecret'
TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NjEzMDY3OTAsIm5iZiI6MTU2MDA5NzE5MCwiZW1haWwiOiJ3b2xmQHRoZWRvb3IuY29tIn0.IpM4VMnqIgOoQeJxUbLT-cRcAjK41jronkVrqRLFmmk'
EMAIL = 'sjoerd.vellinga@gmail.com'
PASSWORD = 'huff-puff'
NEXT = 'Up to the final project |o|  |o|'
MOOD = 'Looking forward to complete this Nanodegree'

@pytest.fixture
def client():
    os.environ['JWT_SECRET'] = SECRET
    main.APP.config['TESTING'] = True
    client = main.APP.test_client()

    yield client



def test_health(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == 'Still healthy ;-)'


def test_auth(client):
    body = {'email': EMAIL,
            'password': PASSWORD}
    response = client.post('/auth', 
                           data=json.dumps(body),
                           content_type='application/json')

    assert response.status_code == 200
    token = response.json['token']
    assert token is not None

class TestApp(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.start_time = datetime.datetime.now()

    @patch('main.datetime')
    def test_app_info_endpoint(self, mock_datetime):
        mock_now = MagicMock(return_value=self.start_time)
        mock_datetime.datetime.now = mock_now

        response = self.client.get('/me')
        self.assertEqual(response.status_code, 200)
        expected_response = f"App Name: Udacity CloudFormation App<br>App Age: 0:00:00"
        self.assertEqual(response.data.decode('utf-8'), expected_response)

if __name__ == '__main__':
    unittest.main()