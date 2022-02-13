from typing import (
    Dict,
    Optional,
)
from pydantic import (
    BaseModel,
    Extra,
)
from .base import BinarySensor, Sensor


COMPONENT_GROUPS = ['sensor', 'binary_sensors']


class ComponentConfig(BaseModel):
    sensor: Optional[Dict[str, Sensor]] = dict()
    binary_sensor: Optional[Dict[str, BinarySensor]] = dict()

    class Config:
        extra = Extra.forbid

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_names()

    def set_names(self):
        for group in COMPONENT_GROUPS:
            for name, component in getattr(self, group, dict()).items():
                component.set_name(name)
