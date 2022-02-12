import unittest
from mqttassistant.dispatch import Signal
from mqttassistant.mqtt import Mqtt
from .test import Callback


class MqttTest(unittest.IsolatedAsyncioTestCase):
    async def test_topic_signal_connect(self):
        signal = Signal()
        mqtt = Mqtt(topic_signal=signal)
        with self.assertLogs('Mqtt', level='DEBUG') as cm:
            await signal.connect('sensor/state', callback=Callback())
            self.assertEqual(mqtt.subscribed_topics, {'sensor/state'})
            self.assertEqual(cm.output, [
                'DEBUG:Mqtt:topic_subscribe: sensor/state',
            ])
            # connecting again does not add another item
            await signal.connect('sensor/state', callback=Callback())
            self.assertEqual(mqtt.subscribed_topics, {'sensor/state'})
            self.assertEqual(cm.output, [
                'DEBUG:Mqtt:topic_subscribe: sensor/state',
            ])
            # connecting another topic does
            await signal.connect('another/state', callback=Callback())
            self.assertEqual(mqtt.subscribed_topics, {'sensor/state', 'another/state'})
            self.assertEqual(cm.output, [
                'DEBUG:Mqtt:topic_subscribe: sensor/state',
                'DEBUG:Mqtt:topic_subscribe: another/state',
            ])

    async def test_topic_signal_disconnect(self):
        signal = Signal()
        mqtt = Mqtt(topic_signal=signal)
        await signal.connect('sensor/state', callback=Callback())
        await signal.connect('another/state', callback=Callback())
        with self.assertLogs('Mqtt', level='DEBUG') as cm:
            await signal.disconnect('sensor/state')
            self.assertEqual(mqtt.subscribed_topics, {'another/state'})
            self.assertEqual(cm.output, [
                'DEBUG:Mqtt:topic_unsubscribe: sensor/state',
            ])
            # disconnecting again does not change anything
            await signal.disconnect('sensor/state')
            self.assertEqual(mqtt.subscribed_topics, {'another/state'})
            self.assertEqual(cm.output, [
                'DEBUG:Mqtt:topic_unsubscribe: sensor/state',
            ])
