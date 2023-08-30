'''
Tests for jwt flask app.
'''
import os
import json
import pytest
import unittest
import main

from flask import Flask
import pytest
from main import APP

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
        self.app = app.test_client()

    def test_next_route(self):
        response = self.app.get('/next')
        print(response.data)  # Add this line to print the response data
        data = json.loads(response.data)
        expected_data = {
            "What is on your mind?": "Looking forward to start with the Final Project ;-)"
        }
        self.assertDictEqual(data, expected_data)
        
if __name__ == '__main__':
    unittest.main()