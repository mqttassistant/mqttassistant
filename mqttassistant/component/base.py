import os
from typing import (
    List,
    Optional,
)
from pydantic import (
    BaseModel,
    Extra,
    Field,
)


class Component(BaseModel):
    availability_topic: Optional[str] = ''
    availability_payload_online: Optional[str] = Field(default_factory=lambda: os.getenv('DEFAULT_AVAILABILITY_PAYLOAD_ONLINE', 'online'))
    availability_payload_offline: Optional[str] = Field(default_factory=lambda: os.getenv('DEFAULT_AVAILABILITY_PAYLOAD_OFFLINE', 'offline'))
    group: Optional[str] = None
    name: Optional[str] = None
    _available: Optional[bool] = False
    _subscribe_topics: Optional[List[str]] = []

    class Config:
        extra = Extra.forbid
        underscore_attrs_are_private = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.availability_topic:
            self._subscribe_topics.append(self.availability_topic)

    def is_optimistic(self) -> bool:
        return not bool(self.availability_topic)

    def is_available(self) -> bool:
        return self._available or self.is_optimistic()

    def get_subscribe_topics(self):
        return self._subscribe_topics

    def set_name(self, name: str):
        self.name = name

    async def _on_mqtt_message_received(self, subject, payload):
        await self.on_mqtt_message_received(subject, payload)

    async def on_mqtt_message_received(self, topic, payload):
        if topic == self.availability_topic:
            if payload == self.availability_payload_online:
                self._available = True
            if payload == self.availability_payload_offline:
                self._available = False


class Sensor(Component):
    group: Optional[str] = 'sensor'
    state_topic: Optional[str] = ''
    state: Optional[float] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.state_topic:
            self._subscribe_topics.append(self.state_topic)

    async def on_mqtt_message_received(self, topic, payload):
        if topic == self.state_topic:
            self.state = float(payload)
        else:
            await super().on_mqtt_message_received(topic, payload)


class BinarySensor(Sensor):
    group: Optional[str] = 'binary_sensor'
    state_payload_on: Optional[str] = Field(default_factory=lambda: os.getenv('DEFAULT_STATE_PAYLOAD_ON', 'ON'))
    state_payload_off: Optional[str] = Field(default_factory=lambda: os.getenv('DEFAULT_STATE_PAYLOAD_OFF', 'OFF'))
    state: Optional[bool] = None

    def is_on(self):
        return bool(self.state)

    def is_off(self):
        return not bool(self.state)

    async def on_mqtt_message_received(self, topic, payload):
        if topic == self.state_topic:
            if payload == self.state_payload_on:
                self.state = True
            if payload == self.state_payload_off:
                self.state = False
        else:
            await super().on_mqtt_message_received(topic, payload)
