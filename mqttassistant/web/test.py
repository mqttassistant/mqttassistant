from fastapi import (
    APIRouter,
    Request,
)
from mqttassistant.dispatch import Signal
from ..config import Config


router = APIRouter(prefix="/test")


@router.get("/component")
async def component(request: Request):
    config: Config = request.app.config
    mqtt_topic_signal: Signal = request.app.mqtt_topic_signal
    group = 'sensor'
    for name, component in config.component.sensor.items():
        for topic in component.get_subscribe_topics():
            uid = '{}-{}-{}'.format(group, name, topic)
            await mqtt_topic_signal.connect(uid, component._on_mqtt_message_received, subject=topic)
    return config.component
