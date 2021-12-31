import asyncio


class Application:
    def __init__(self, **kwargs):
        pass

    def start(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.run())
        loop.run_forever()

    async def run(self):
        pass
