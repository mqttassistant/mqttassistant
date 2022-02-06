import asyncio
from collections.abc import Callable
from typing import (
    List,
    Optional,
)


class Signal:
    def __init__(self, connect_callback: Optional[Callable] = None, disconnect_callback: Optional[Callable] = None):
        self.connect_callback = connect_callback
        self.disconnect_callback = disconnect_callback
        self.callback = dict()
        self.subject_callback = dict()

    async def connect(self, uid: str, callback: Callable, subject: Optional[str] = None):
        assert callable(callback)
        connected = False
        if subject:
            self.subject_callback[subject] = self.subject_callback.get('subject', dict())
            if uid not in self.subject_callback[subject]:
                self.subject_callback[subject][uid] = callback
                connected = True
        else:
            if uid not in self.callback:
                self.callback[uid] = callback
                connected = True
        if connected and self.connect_callback:
            await self.connect_callback(uid=uid, subject=subject)
        return connected

    async def disconnect(self, uid: str, subject: Optional[str] = None):
        disconnected = False
        if subject:
            if subject in self.subject_callback:
                if uid in self.subject_callback[subject]:
                    del self.subject_callback[subject][uid]
                if not self.subject_callback[subject]:
                    del self.subject_callback[subject]
                disconnected = True
        else:
            if uid in self.callback:
                del self.callback[uid]
                disconnected = True
        if disconnected and self.disconnect_callback:
            await self.disconnect_callback(uid=uid, subject=subject)
        return disconnected

    def get_callbacks(self, subject: str) -> List[Callable]:
        return [x for x in self.callback.values()] + [x for x in self.subject_callback.get(subject, dict()).values()]

    async def send(self, subject: str, **kwargs) -> None:
        awaitables = [c(subject=subject, **kwargs) for c in self.get_callbacks(subject)]
        return await asyncio.gather(*awaitables)
