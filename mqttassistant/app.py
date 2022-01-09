import asyncio
import signal
from .log import get_logger
from . import web


class Application:
    def __init__(self, **kwargs):
        self.log = get_logger('App')
        self.running = asyncio.Future()
        # Web server
        self.web = web.Server(**kwargs)

    def start(self):
        self.log.info('started')
        self.loop = asyncio.get_event_loop()
        self.loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(self.stop()))
        self.loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.create_task(self.stop()))
        self.loop.create_task(self.run())
        self.loop.run_until_complete(self.running)

    async def run(self):
        # Web server
        self.web_task = self.web.run()
        self.loop.create_task(self.web_task)

    async def stop(self):
        self.log.info('stopping')
        await self.web.stop()
        self.running.set_result(False)
        self.log.info('stopped')
