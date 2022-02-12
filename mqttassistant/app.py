import asyncio
import signal
from . import mqtt
from . import web
from .config import Config
from .dispatch import Signal
from .log import get_logger
from .warn import configure_warnings


configure_warnings()


class Application:
    def __init__(self, **kwargs):
        self.log = get_logger('App')
        self.running = asyncio.Future()
        # Config
        self.config = Config.parse_config_path(path=kwargs['config_path'])
        # Signals
        self.mqtt_topic_signal = Signal()
        # Mqtt client
        self.mqtt = mqtt.Mqtt(topic_signal=self.mqtt_topic_signal, **kwargs)
        # Web server
        self.web = web.Server(app_config=self.config, **kwargs)

    def start(self):
        self.log.info('started')
        self.loop = asyncio.get_event_loop()
        self.loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(self.stop()))
        self.loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.create_task(self.stop()))
        self.loop.create_task(self.run())
        self.loop.run_until_complete(self.running)

    async def run(self):
        # Mqtt client
        self.mqtt_task = self.mqtt.run()
        self.loop.create_task(self.mqtt_task)
        # Web server
        self.web_task = self.web.run()
        self.loop.create_task(self.web_task)

    async def stop(self):
        self.log.info('stopping')
        await self.web.stop()
        await self.mqtt.stop()
        self.running.set_result(False)
        self.log.info('stopped')
