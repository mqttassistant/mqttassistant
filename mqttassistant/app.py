import asyncio
from .log import get_logger


logger = get_logger('Application')


class Application:
    def __init__(self, **kwargs):
        pass

    def start(self):
        logger.info('start')
        loop = asyncio.get_event_loop()
        loop.create_task(self.run())
        loop.run_forever()

    def stop(self):
        logger.info('stop')

    async def run(self):
        pass
