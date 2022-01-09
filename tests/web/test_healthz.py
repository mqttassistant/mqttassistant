import unittest
from fastapi.testclient import TestClient
from mqttassistant.web import App


client = TestClient(App())


class HealthzTest(unittest.TestCase):
    def test_main(self):
        response = client.get('/healthz')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'')
