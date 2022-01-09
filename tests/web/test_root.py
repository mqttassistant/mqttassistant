import unittest
from fastapi.testclient import TestClient
from mqttassistant.web import App


client = TestClient(App())


class RootTest(unittest.TestCase):
    def test_home(self):
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
