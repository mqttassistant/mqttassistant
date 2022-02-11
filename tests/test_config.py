import unittest
from mqttassistant.auth import Auth
from mqttassistant.config import Config

class ConfigTest(unittest.TestCase):
    
    def test_user_config(self):
        config = dict(users=[
            dict(username='user1', password='hashed_passwd1'),
            dict(username='user2', password='hashed_passwd1')
        ])
        user_config = Config.parse_obj(config)
        self.assertEqual(user_config.users[0].username, 'user1')
        self.assertEqual(user_config.users[1].username, 'user2')
        self.assertEqual(len(user_config.users), 2)

    def test_auth_config_default(self):
        config = dict()
        config = Config.parse_obj(config)
        auth = config.auth
        self.assertIsInstance(auth, Auth)
        self.assertEqual(auth.secret_key, '')
        self.assertEqual(auth.algorithm, 'HS256')
        self.assertEqual(auth.access_token_expire_minutes, 30)

    def test_auth_config_custom(self):
        config = dict(auth=dict(
            secret_key='secret_key',
            algorithm='algorithm',
            access_token_expire_minutes=2
        ))
        config = Config.parse_obj(config)
        auth = config.auth
        self.assertIsInstance(auth, Auth)
        self.assertEqual(auth.secret_key, 'secret_key')
        self.assertEqual(auth.algorithm, 'algorithm')
        self.assertEqual(auth.access_token_expire_minutes, 2)

