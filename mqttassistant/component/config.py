from typing import (
    Dict,
    Optional,
)
from pydantic import (
    BaseModel,
    Extra,
)
from .base import BinarySensor, Sensor


class ComponentConfig(BaseModel):
    sensor: Optional[Dict[str, Sensor]] = dict()
    binary_sensor: Optional[Dict[str, BinarySensor]] = dict()

    class Config:
        extra = Extra.forbid
