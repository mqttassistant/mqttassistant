import unittest
from fastapi.testclient import TestClient
from mqttassistant.web import App

app_config = dict(
    auth=dict(
        users=dict(
            user1=dict(
                username='user1',
                password='$2b$12$XTT6OTxJSGJ0y36iOh5y7Ofy5CwCxHBsty8QWTr4UDl.ylM80ZrTy'
            )
        )
    )
)
client = TestClient(App(web_config=app_config))


class LoginTest(unittest.TestCase):

    def test_api_login_ok(self):
        response = client.post('/login', json=dict(username='user1', password='user1'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(len(response.json()['token']), 131)
        
    def test_api_login_ko(self):

        response = client.post('/login', json=dict(username='user1', password='bad_password'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), dict(detail='Incorrect username or password'))