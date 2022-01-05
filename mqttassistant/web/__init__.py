import asyncio
import os
import signal
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRoute
from hypercorn.asyncio import serve
from hypercorn.config import Config
from . import root
from ..log import get_logger


class App(FastAPI):
    def __init__(self):
        module_path = os.path.dirname(os.path.realpath(__file__))
        super().__init__(routes=[
            APIRoute('/', root.home),
        ])
        self.templates = Jinja2Templates(directory=os.path.join(module_path, 'templates'))


class Server:
    def __init__(self, web_host='0.0.0.0', web_port=8000, **kwargs):
        self.log = get_logger('Web')
        self.host = web_host
        self.port = web_port
        # Hypercorn
        self.task = None
        self.shutdown_event = asyncio.Event()
        self.config = Config()
        self.config.bind = ['{}:{}'.format(self.host, self.port)]
        self.config.accesslog = self.log
        self.config.errorlog = self.log
        self.config.access_log_format = '%(h)s %(l)s %(l)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)s'
        self.app = App()

    def shutdown_signal_handler(self, *args) -> None:
            self.shutdown_event.set()

    async def start(self, logger=None):
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGTERM, self.shutdown_signal_handler)
        self.task = asyncio.create_task(
            serve(
                self.app,
                self.config,
                shutdown_trigger=self.shutdown_event.wait,
            )
        )

    async def stop(self, logger=None):
        self.task.cancel()
        self.log.info('stopped')
