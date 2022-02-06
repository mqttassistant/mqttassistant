import asyncio


class Callback:
    def __init__(self, delay=0):
        self.delay = delay
        self.called = []

    async def __call__(self, **kwargs):
        await asyncio.sleep(self.delay)
        self.called.append(kwargs)
        return kwargs
