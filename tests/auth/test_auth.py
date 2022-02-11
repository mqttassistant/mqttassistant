import unittest
from mqttassistant.auth import Auth, User
from mqttassistant.web import App
from typing import (
    List
)

auth=Auth()

class AuthTest(unittest.TestCase):
    def test_get_password_hash(self):
        hashed_password = auth.get_password_hash('password_test')
        user = User(username='user1', password=hashed_password)
        self.assertTrue(auth.verify_password('password_test', hashed_password))
    
    def test_verify_password(self): 
        hashed_password = auth.get_password_hash('right_password')
        user = User(username='user1', password=hashed_password)   
        self.assertTrue(auth.verify_password('right_password', user.password))
        self.assertFalse(auth.verify_password('bad_password', user.password))
          
        with self.assertRaises(Exception) as e:
            auth.verify_password('right_password', 'bad_ashed_password')
        self.assertEqual(e.exception.args, ('hash could not be identified', None))

    def test_authenticate(self):
        hashed_password = auth.get_password_hash('password')
        user = User(username='user', password=hashed_password)
        self.assertFalse(auth.authenticate(user,'bad_password'))
        auth_user = auth.authenticate(user,'password')
        self.assertIsInstance(auth_user, User)
        self.assertEqual(auth_user.password, hashed_password)

    def test_decode_token_ok(self):
        hashed_password = auth.get_password_hash('password')
        user = User(username='user', password=hashed_password)
        username = auth.decode_token(auth.encode_token(user))
        self.assertEqual(username, 'user')

    def test_decode_token_ko(self):
        hashed_password = auth.get_password_hash('password')
        user = User(username='user', password=hashed_password)
        
        with self.assertRaises(Exception) as e:
            auth.decode_token('Bad token')
        self.assertEqual(e.exception.detail, ('Could not validate credentials'))
        
    