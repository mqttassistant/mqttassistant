import asyncio
import os
from typing import Optional
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRoute
from hypercorn.asyncio import serve
from hypercorn.config import Config
from . import healthz
from . import root
from ..config import Config as AppConfig
from ..dispatch import Signal
from ..log import get_logger


class App(FastAPI):
    def __init__(self, config: Optional[AppConfig] = AppConfig(), mqtt_topic_signal: Optional[AppConfig] = Signal(), **kwargs):
        module_path = os.path.dirname(os.path.realpath(__file__))
        self.config = config
        self.mqtt_topic_signal = mqtt_topic_signal

        super().__init__(
            routes=[
                APIRoute('/', root.home),
                APIRoute('/healthz', healthz.main),
                APIRoute('/login', root.login, methods=['POST']),
            ],
            **kwargs
        )
        self.templates = Jinja2Templates(directory=os.path.join(module_path, 'templates'))
        # ------------------------------------------------------
        # TO BE REMOVED
        # ------------------------------------------------------
        from . import test
        self.include_router(test.router)
        # ------------------------------------------------------


class Server:
    def __init__(self, web_host='0.0.0.0', web_port=8000, app_config: Optional[AppConfig] = AppConfig(), mqtt_topic_signal: Optional[AppConfig] = Signal(), **kwargs):
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
        self.app = App(config=app_config, mqtt_topic_signal=mqtt_topic_signal, **kwargs)

    def run(self):
        return serve(
            self.app,
            self.config,
            shutdown_trigger=self.shutdown_event.wait,
        )

    async def stop(self):
        self.log.info('stopped')
