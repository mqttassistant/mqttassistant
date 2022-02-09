import unittest
from mqttassistant.web.auth import Auth
from mqttassistant.web import App


class AuthTest(unittest.TestCase):

    def test_init_users(self):
        auth = Auth(users={
            'user1': dict(username='user1', password='$2b$12$XTT6OTxJSGJ0y36iOh5y7Ofy5CwCxHBsty8QWTr4UDl.ylM80ZrTy')
        })
        self.assertEqual(len(auth.users), 1)
        self.assertEqual(auth.users['user1']['password'], '$2b$12$XTT6OTxJSGJ0y36iOh5y7Ofy5CwCxHBsty8QWTr4UDl.ylM80ZrTy')
        self.assertNotIn('user2', auth.users)
        
    def test_get_user(self):
        auth = Auth(users={
            'user1': dict(username='user1', password='$2b$12$XTT6OTxJSGJ0y36iOh5y7Ofy5CwCxHBsty8QWTr4UDl.ylM80ZrTy'),
            'user2': dict(username='user2', password='$2b$12$XTT6OTxJSGJ0y36iOh5y7Ofy5CwCxHBsty8QWTr4UDl.ylM80ZrT2')
        })
        self.assertEqual(auth.get_user('user1').password, '$2b$12$XTT6OTxJSGJ0y36iOh5y7Ofy5CwCxHBsty8QWTr4UDl.ylM80ZrTy')
        self.assertEqual(auth.get_user('user2').password, '$2b$12$XTT6OTxJSGJ0y36iOh5y7Ofy5CwCxHBsty8QWTr4UDl.ylM80ZrT2')
        self.assertFalse(auth.get_user('user12'))

    def test_authenticate(self):
        auth = Auth(users={
            'user1': dict(username='user1', password='$2b$12$XTT6OTxJSGJ0y36iOh5y7Ofy5CwCxHBsty8QWTr4UDl.ylM80ZrTy'),
            'user2': dict(username='user2', password='Bad Password')
        })
        self.assertFalse(auth.authenticate('user1','test'))
        with self.assertRaises(Exception) as e:
            self.assertFalse(auth.authenticate('user2','test'))
        self.assertEqual(e.exception.args, ('hash could not be identified', None))
        self.assertIsInstance(auth.authenticate('user1','user1'), object)
        self.assertEqual(auth.authenticate('user1','user1').password, '$2b$12$XTT6OTxJSGJ0y36iOh5y7Ofy5CwCxHBsty8QWTr4UDl.ylM80ZrTy')


