import os
import unittest
from unittest.mock import patch
from mqttassistant.component.base import (
    BinarySensor,
    Component,
    Sensor,
)


class ComponentTest(unittest.TestCase):
    def test_subscribe_topics_no_availability_topic(self):
        component = Component()
        self.assertEqual(component._subscribe_topics, [])

    def test_subscribe_topics_availability_topic(self):
        component = Component(availability_topic='available/state')
        self.assertEqual(component._subscribe_topics, ['available/state'])

    def test_is_optimistic_true(self):
        component = Component()
        self.assertTrue(component.is_optimistic())
        component = Component(availability_topic='')
        self.assertTrue(component.is_optimistic())

    def test_is_optimistic_false(self):
        component = Component(availability_topic='availability')
        self.assertFalse(component.is_optimistic())

    def test_is_available_optimistic(self):
        'If no availability_topic is provided we assume (hope) that the component is available'
        component = Component()
        self.assertTrue(component.is_available())

    def test_is_available_true(self):
        component = Component(availability_topic='availability')
        component._available = True
        self.assertTrue(component.is_available())

    def test_is_available_false(self):
        component = Component(availability_topic='availability')
        component._available = False
        self.assertFalse(component.is_available())

    def test_is_available_default(self):
        component = Component(availability_topic='availability')
        self.assertFalse(component.is_available())

    def test_payload_online_default(self):
        component = Component()
        self.assertEqual(component.availability_payload_online, 'online')

    def test_payload_offline_default(self):
        component = Component()
        self.assertEqual(component.availability_payload_offline, 'offline')

    @patch.dict(os.environ, dict(DEFAULT_AVAILABILITY_PAYLOAD_ONLINE='ON'))
    def test_payload_online_default_override(self):
        component = Component()
        self.assertEqual(component.availability_payload_online, 'ON')

    @patch.dict(os.environ, dict(DEFAULT_AVAILABILITY_PAYLOAD_OFFLINE='OFF'))
    def test_payload_offline_default_override(self):
        component = Component()
        self.assertEqual(component.availability_payload_offline, 'OFF')


class SensorTest(unittest.TestCase):
    def test_state_empty(self):
        component = Sensor()
        self.assertEqual(component.state, None)

    def test_subscribe_topics_availability(self):
        component = Sensor(availability_topic='available/state')
        self.assertEqual(component._subscribe_topics, ['available/state'])

    def test_subscribe_topics_availability_status(self):
        component = Sensor(availability_topic='available/state', state_topic='state')
        self.assertEqual(component._subscribe_topics, ['available/state', 'state'])



class BinarySensorTest(unittest.TestCase):
    def test_subscribe_topics_availability_status(self):
        component = BinarySensor(availability_topic='available/state', state_topic='state')
        self.assertEqual(component._subscribe_topics, ['available/state', 'state'])

    def test_payload_on_default(self):
        component = BinarySensor()
        self.assertEqual(component.state_payload_on, 'ON')

    def test_payload_off_default(self):
        component = BinarySensor()
        self.assertEqual(component.state_payload_off, 'OFF')

    @patch.dict(os.environ, dict(DEFAULT_STATE_PAYLOAD_ON='yes'))
    def test_payload_on_default_override(self):
        component = BinarySensor()
        self.assertEqual(component.state_payload_on, 'yes')

    @patch.dict(os.environ, dict(DEFAULT_STATE_PAYLOAD_OFF='no'))
    def test_payload_off_default_override(self):
        component = BinarySensor()
        self.assertEqual(component.state_payload_off, 'no')

    def test_state_none(self):
        component = BinarySensor()
        self.assertFalse(component.is_on())
        self.assertTrue(component.is_off())

    def test_state_true(self):
        component = BinarySensor(state=True)
        self.assertTrue(component.is_on())
        self.assertFalse(component.is_off())

    def test_state_false(self):
        component = BinarySensor(state=False)
        self.assertFalse(component.is_on())
        self.assertTrue(component.is_off())
