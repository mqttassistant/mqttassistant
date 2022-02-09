import asyncio
import signal
from . import mqtt
from . import web
from .config import Config
from .log import get_logger


class Application:
    def __init__(self, **kwargs):
        self.log = get_logger('App')
        self.running = asyncio.Future()
        # Config
        self.config = Config.parse_config_path(path=kwargs['config_path'])
        # Mqtt client
        self.mqtt = mqtt.Mqtt(**kwargs)
        # Web server
        kwargs.update('web_config', self.config)
        self.web = web.Server(**kwargs)

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
