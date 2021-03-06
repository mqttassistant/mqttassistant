import os
import unittest
from unittest.mock import patch
from mqttassistant.component.base import (
    BinarySensor,
    Component,
    Sensor,
)
from mqttassistant.component.config import ComponentConfig


class ComponentConfigTest(unittest.TestCase):
    def test_names(self):
        sensor = Sensor()
        self.assertEqual(sensor.name, None)
        ComponentConfig(sensor=dict(myname=sensor))
        self.assertEqual(sensor.name, 'myname')


class ComponentTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.component_class = Component

    def test_group(self):
        component = self.component_class()
        self.assertEqual(component.group, None)

    def test_name(self):
        component = self.component_class()
        self.assertEqual(component.name, None)
        component.set_name('component-name')
        self.assertEqual(component.name, 'component-name')

    def test_subscribe_topics_no_availability_topic(self):
        component = self.component_class()
        self.assertEqual(component._subscribe_topics, [])

    def test_subscribe_topics_availability_topic(self):
        component = self.component_class(availability_topic='available/state')
        self.assertEqual(component._subscribe_topics, ['available/state'])

    def test_is_optimistic_true(self):
        component = self.component_class()
        self.assertTrue(component.is_optimistic())
        component = self.component_class(availability_topic='')
        self.assertTrue(component.is_optimistic())

    def test_is_optimistic_false(self):
        component = self.component_class(availability_topic='availability')
        self.assertFalse(component.is_optimistic())

    def test_is_available_optimistic(self):
        'If no availability_topic is provided we assume (hope) that the component is available'
        component = self.component_class()
        self.assertTrue(component.is_available())

    def test_is_available_true(self):
        component = self.component_class(availability_topic='availability')
        component._available = True
        self.assertTrue(component.is_available())

    def test_is_available_false(self):
        component = self.component_class(availability_topic='availability')
        component._available = False
        self.assertFalse(component.is_available())

    def test_is_available_default(self):
        component = self.component_class(availability_topic='availability')
        self.assertFalse(component.is_available())

    def test_payload_online_default(self):
        component = self.component_class()
        self.assertEqual(component.availability_payload_online, 'online')

    def test_payload_offline_default(self):
        component = self.component_class()
        self.assertEqual(component.availability_payload_offline, 'offline')

    @patch.dict(os.environ, dict(DEFAULT_AVAILABILITY_PAYLOAD_ONLINE='ON'))
    def test_payload_online_default_override(self):
        component = self.component_class()
        self.assertEqual(component.availability_payload_online, 'ON')

    @patch.dict(os.environ, dict(DEFAULT_AVAILABILITY_PAYLOAD_OFFLINE='OFF'))
    def test_payload_offline_default_override(self):
        component = self.component_class()
        self.assertEqual(component.availability_payload_offline, 'OFF')

    def test_get_subscribe_topics_empty(self):
        component = self.component_class()
        self.assertEqual(component.get_subscribe_topics(), [])

    def test_get_subscribe_topics_availability(self):
        component = self.component_class(availability_topic='availability')
        self.assertEqual(component.get_subscribe_topics(), ['availability'])

    async def test_on_mqtt_message_received(self):
        component = self.component_class(availability_topic='availability')
        await component._on_mqtt_message_received('availability', 'online')
        self.assertTrue(component.is_available())

    async def test_availability_online(self):
        component = self.component_class(availability_topic='availability')
        await component.on_mqtt_message_received('availability', 'online')
        self.assertTrue(component.is_available())

    async def test_availability_offline(self):
        component = self.component_class(availability_topic='availability')
        await component.on_mqtt_message_received('availability', 'offline')
        self.assertFalse(component.is_available())


class SensorTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.component_class = Sensor

    def test_group(self):
        component = self.component_class()
        self.assertEqual(component.group, 'sensor')

    def test_name(self):
        component = self.component_class()
        self.assertEqual(component.name, None)
        component.set_name('component-name')
        self.assertEqual(component.name, 'component-name')

    def test_state_empty(self):
        component = self.component_class()
        self.assertEqual(component.state, None)

    def test_subscribe_topics_availability(self):
        component = self.component_class(availability_topic='available/state')
        self.assertEqual(component._subscribe_topics, ['available/state'])

    def test_subscribe_topics_availability_status(self):
        component = self.component_class(availability_topic='available/state', state_topic='state')
        self.assertEqual(component._subscribe_topics, ['available/state', 'state'])

    def test_get_subscribe_topics_availability_state(self):
        component = self.component_class(availability_topic='availability', state_topic='state')
        self.assertEqual(component.get_subscribe_topics(), ['availability', 'state'])

    def test_get_subscribe_topics_state(self):
        component = self.component_class(state_topic='state')
        self.assertEqual(component.get_subscribe_topics(), ['state'])

    async def test_availability_online(self):
        component = self.component_class(availability_topic='availability')
        await component.on_mqtt_message_received('availability', 'online')
        self.assertTrue(component.is_available())

    async def test_availability_offline(self):
        component = self.component_class(availability_topic='availability')
        await component.on_mqtt_message_received('availability', 'offline')
        self.assertFalse(component.is_available())

    async def test_event_state(self):
        component = self.component_class(state_topic='state')
        await component.on_mqtt_message_received('state', '42')
        self.assertEqual(component.state, 42)


class BinarySensorTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.component_class = BinarySensor

    def test_group(self):
        component = self.component_class()
        self.assertEqual(component.group, 'binary_sensor')

    def test_name(self):
        component = self.component_class()
        self.assertEqual(component.name, None)
        component.set_name('component-name')
        self.assertEqual(component.name, 'component-name')

    def test_subscribe_topics_availability_status(self):
        component = self.component_class(availability_topic='available/state', state_topic='state')
        self.assertEqual(component._subscribe_topics, ['available/state', 'state'])

    def test_payload_on_default(self):
        component = self.component_class()
        self.assertEqual(component.state_payload_on, 'ON')

    def test_payload_off_default(self):
        component = self.component_class()
        self.assertEqual(component.state_payload_off, 'OFF')

    @patch.dict(os.environ, dict(DEFAULT_STATE_PAYLOAD_ON='yes'))
    def test_payload_on_default_override(self):
        component = self.component_class()
        self.assertEqual(component.state_payload_on, 'yes')

    @patch.dict(os.environ, dict(DEFAULT_STATE_PAYLOAD_OFF='no'))
    def test_payload_off_default_override(self):
        component = self.component_class()
        self.assertEqual(component.state_payload_off, 'no')

    def test_state_none(self):
        component = self.component_class()
        self.assertFalse(component.is_on())
        self.assertTrue(component.is_off())

    def test_state_true(self):
        component = self.component_class(state=True)
        self.assertTrue(component.is_on())
        self.assertFalse(component.is_off())

    def test_state_false(self):
        component = self.component_class(state=False)
        self.assertFalse(component.is_on())
        self.assertTrue(component.is_off())

    def test_get_subscribe_topics_availability_state(self):
        component = self.component_class(availability_topic='availability', state_topic='state')
        self.assertEqual(component.get_subscribe_topics(), ['availability', 'state'])

    async def test_availability_online(self):
        component = self.component_class(availability_topic='availability')
        await component.on_mqtt_message_received('availability', 'online')
        self.assertTrue(component.is_available())

    async def test_availability_offline(self):
        component = self.component_class(availability_topic='availability')
        await component.on_mqtt_message_received('availability', 'offline')
        self.assertFalse(component.is_available())

    async def test_event_on(self):
        component = self.component_class(state_topic='state')
        await component.on_mqtt_message_received('state', 'ON')
        self.assertTrue(component.state)

    async def test_event_off(self):
        component = self.component_class(state_topic='state')
        await component.on_mqtt_message_received('state', 'OFF')
        self.assertFalse(component.state)
