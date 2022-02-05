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


class Sensor(Component):
    state_topic: Optional[str] = ''
    state: Optional[float] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.state_topic:
            self._subscribe_topics.append(self.state_topic)


class BinarySensor(Sensor):
    state_payload_on: Optional[str] = Field(default_factory=lambda: os.getenv('DEFAULT_STATE_PAYLOAD_ON', 'ON'))
    state_payload_off: Optional[str] = Field(default_factory=lambda: os.getenv('DEFAULT_STATE_PAYLOAD_OFF', 'OFF'))
    state: Optional[bool] = None

    def is_on(self):
        return bool(self.state)

    def is_off(self):
        return not bool(self.state)
