import os
import unittest
from unittest.mock import patch
from mqttassistant.component import Component


class ComponentTest(unittest.TestCase):
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
        self.assertEqual(component._availability_payload_online, 'online')

    def test_payload_offline_default(self):
        component = Component()
        self.assertEqual(component._availability_payload_offline, 'offline')

    @patch.dict(os.environ, dict(DEFAULT_AVAILABILITY_PAYLOAD_ONLINE='ON'))
    def test_payload_online_default_override(self):
        component = Component()
        self.assertEqual(component._availability_payload_online, 'ON')

    @patch.dict(os.environ, dict(DEFAULT_AVAILABILITY_PAYLOAD_OFFLINE='OFF'))
    def test_payload_offline_default_override(self):
        component = Component()
        self.assertEqual(component._availability_payload_offline, 'OFF')
