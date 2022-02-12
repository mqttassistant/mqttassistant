import unittest
from fastapi.testclient import TestClient
from mqttassistant.config import Config
from mqttassistant.component import Sensor
from mqttassistant.dispatch import Signal
from mqttassistant.web import App
from ..test import Callback


class ComponentTest(unittest.IsolatedAsyncioTestCase):
    async def test_get(self):
        sensor = Sensor(state_topic='sensor/state')
        config = Config()
        config.component.sensor = dict(sensor=sensor)
        callback = Callback()
        mqtt_topic_signal = Signal(connect_callback=callback)
        # client
        client = TestClient(App(config=config, mqtt_topic_signal=mqtt_topic_signal))
        self.assertEqual(callback.called, [])
        # get
        response = client.get('/test/component')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(callback.called, [dict(subject='sensor/state', uid='sensor-sensor-sensor/state')])
        # Simulate mqtt sending a message
        await mqtt_topic_signal.send(subject='sensor/state', payload='42')
        self.assertEqual(sensor.state, 42)
