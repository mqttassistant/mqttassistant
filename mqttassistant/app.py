import asyncio
import signal
from .log import get_logger


logger = get_logger('Application')


class Application:
    def __init__(self, **kwargs):
        self.running = asyncio.Future()

    def start(self):
        logger.info('start')
        self.loop = asyncio.get_event_loop()
        self.loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(self.stop()))
        self.loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.create_task(self.stop()))
        self.loop.create_task(self.run())
        self.loop.run_until_complete(self.running)


    async def stop(self):
        logger.info('stop')
        self.running.set_result(False)

    async def run(self):
        pass
