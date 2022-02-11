import unittest
from fastapi.testclient import TestClient
from mqttassistant.web import App
from mqttassistant.auth import Auth, User
from mqttassistant.config import Config

auth = Auth()
app_config = dict(
    users=[
        User(username='user', password=auth.get_password_hash('password'))
    ],
    auth=auth
)
client = TestClient(App(config=Config.parse_obj(app_config)))


class RootTest(unittest.TestCase):
    def test_home_no_login(self):
        response = client.get('/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'detail': 'Not authenticated'})

    def test_home_ok(self):
        response = client.post('/login', json=dict(username='user', password='password'))
        token = response.json()['token']
        response = client.get('/', headers={"Authorization": "Bearer {}".format(token)})
        self.assertEqual(response.status_code, 200)


class LoginTest(unittest.TestCase):
  
    def test_api_login_ok(self):
        response = client.post('/login', json=dict(username='user', password='password'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)
        self.assertIsInstance(response.json()['token'], str)
        
    def test_api_login_bad_password(self):
        response = client.post('/login', json=dict(username='user', password='bad_password'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), dict(detail='Incorrect username or password'))

    def test_api_login_user_not_exists(self):
        response = client.post('/login', json=dict(username='bad_user', password='password'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), dict(detail='Incorrect username or password'))