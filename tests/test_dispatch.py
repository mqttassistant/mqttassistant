import unittest
from mqttassistant.dispatch import Signal
from .test import Callback


class SignalTest(unittest.IsolatedAsyncioTestCase):
    async def test_connect(self):
        callback = Callback()
        signal = Signal()
        connected = await signal.connect('abc', callback)
        self.assertTrue(connected)
        self.assertEqual(signal.callback, dict(abc=callback))
        self.assertEqual(signal.subject_callback, dict())
        connected = await signal.connect('abc', callback)
        self.assertFalse(connected)
        self.assertEqual(signal.callback, dict(abc=callback))
        self.assertEqual(signal.subject_callback, dict())

    async def test_connect_subject(self):
        callback = Callback()
        signal = Signal()
        connected = await signal.connect('abc', callback, subject='subject')
        self.assertTrue(connected)
        self.assertEqual(signal.callback, dict())
        self.assertEqual(signal.subject_callback, dict(subject=dict(abc=callback)))
        connected = await signal.connect('abc', callback, subject='subject')
        self.assertFalse(connected)
        self.assertEqual(signal.callback, dict())
        self.assertEqual(signal.subject_callback, dict(subject=dict(abc=callback)))

    async def test_disconnect(self):
        callback = Callback()
        signal = Signal()
        await signal.connect('abc', callback)
        self.assertEqual(signal.callback, dict(abc=callback))
        disconnected = await signal.disconnect('abc')
        self.assertTrue(disconnected)
        self.assertEqual(signal.callback, dict())
        disconnected = await signal.disconnect('abc')
        self.assertFalse(disconnected)
        self.assertEqual(signal.callback, dict())

    async def test_disconnect_subject(self):
        callback = Callback()
        signal = Signal()
        await signal.connect('abc', callback, subject='subject')
        self.assertEqual(signal.subject_callback, dict(subject=dict(abc=callback)))
        disconnected = await signal.disconnect('abc', subject='subject')
        self.assertTrue(disconnected)
        self.assertEqual(signal.subject_callback, dict())
        disconnected = await signal.disconnect('abc', subject='subject')
        self.assertFalse(disconnected)
        self.assertEqual(signal.subject_callback, dict())

    async def test_get_callbacks(self):
        callback_1 = Callback()
        callback_2 = Callback()
        callback_3 = Callback()
        callback_4 = Callback()
        signal = Signal()
        await signal.connect('abc', callback_1)
        await signal.connect('abc', callback_2, subject='subject_2')
        await signal.connect('abc', callback_3, subject='subject_3')
        await signal.connect('123', callback_4)
        callbacks = signal.get_callbacks('subject_2')
        self.assertIsInstance(callbacks, list)
        self.assertIn(callback_1, callbacks)
        self.assertIn(callback_2, callbacks)
        self.assertNotIn(callback_3, callbacks)
        self.assertIn(callback_4, callbacks)
        self.assertEqual(len(callbacks), 3)

    async def test_send_ok(self):
        callback_1 = Callback()
        callback_2 = Callback()
        callback_3 = Callback()
        signal = Signal()
        await signal.connect('uid_1', callback_1)
        await signal.connect('uid_2', callback_2, subject='subject_2')
        await signal.connect('uid_3', callback_3, subject='subject_3')
        await signal.send('subject_2', text='hello')
        self.assertEqual(callback_1.called, [dict(subject='subject_2', text='hello')])
        self.assertEqual(callback_2.called, [dict(subject='subject_2', text='hello')])
        self.assertEqual(callback_3.called, [])

    async def test_send_ko(self):
        async def callback(**kwargs):
            raise Exception('something went wrong')
        signal = Signal()
        await signal.connect('uid', callback)
        with self.assertRaises(Exception) as cm:
            await signal.send('subject', text='hello')
        self.assertEqual(cm.exception.args, ('something went wrong',))

    async def test_connect_callback(self):
        callback = Callback()
        signal = Signal(connect_callback=callback)
        await signal.connect('uid', Callback())
        self.assertEqual(callback.called, [dict(uid='uid', subject=None)])
        # Connecting again does not fire callback
        await signal.connect('uid', Callback())
        self.assertEqual(callback.called, [dict(uid='uid', subject=None)])

    async def test_connect_callback_subject(self):
        callback = Callback()
        signal = Signal(connect_callback=callback)
        await signal.connect('uid', Callback(), subject='subject')
        self.assertEqual(callback.called, [dict(subject='subject', uid='uid')])
        # Connecting again does not fire callback
        await signal.connect('uid', Callback(), subject='subject')
        self.assertEqual(callback.called, [dict(subject='subject', uid='uid')])

    async def test_disconnect_callback(self):
        callback = Callback()
        signal = Signal(disconnect_callback=callback)
        await signal.connect('uid', Callback())
        await signal.disconnect('uid')
        self.assertEqual(callback.called, [dict(uid='uid', subject=None)])
        # Disconnecting again does not fire callback
        await signal.disconnect('uid')
        self.assertEqual(callback.called, [dict(uid='uid', subject=None)])

    async def test_disconnect_callback_subject(self):
        callback = Callback()
        signal = Signal(disconnect_callback=callback)
        await signal.connect('uid', Callback(), subject='subject')
        await signal.disconnect('uid', subject='subject')
        self.assertEqual(callback.called, [dict(subject='subject', uid='uid')])
        # Disconnecting again does not fire callback
        await signal.disconnect('uid', subject='subject')
        self.assertEqual(callback.called, [dict(subject='subject', uid='uid')])
