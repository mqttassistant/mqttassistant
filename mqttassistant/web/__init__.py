import asyncio
import os
from typing import Optional
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from hypercorn.asyncio import serve
from hypercorn.config import Config
from . import healthz
from . import root
from ..config import Config as AppConfig
from ..dispatch import Signal
from ..log import get_logger


class App(FastAPI):
    def __init__(self, config: Optional[AppConfig] = AppConfig(), mqtt_topic_signal: Optional[AppConfig] = Signal(), ui_path: str = '', **kwargs):
        module_path = os.path.dirname(os.path.realpath(__file__))
        self.config = config
        self.mqtt_topic_signal = mqtt_topic_signal

        super().__init__(
            routes=[
                APIRoute('/healthz', healthz.main),
                APIRoute('/login', root.login, methods=['POST']),
            ],
            **kwargs
        )
        if ui_path:
            self.mount('/', StaticFiles(directory=ui_path, html=True), name='ui')
        self.templates = Jinja2Templates(directory=os.path.join(module_path, 'templates'))
        # ------------------------------------------------------
        # TO BE REMOVED
        # ------------------------------------------------------
        from . import test
        self.include_router(test.router)
        # ------------------------------------------------------


class Server:
    def __init__(self, web_host='0.0.0.0', web_port=8000, app_config: Optional[AppConfig] = AppConfig(), mqtt_topic_signal: Optional[AppConfig] = Signal(), **kwargs):
        self.logger = get_logger('Web', level=kwargs.get('log_level', 'INFO'))
        self.host = web_host
        self.port = web_port
        # Hypercorn
        self.task = None
        self.shutdown_event = asyncio.Event()
        self.config = Config()
        self.config.bind = ['{}:{}'.format(self.host, self.port)]
        self.config.accesslog = self.logger
        self.config.errorlog = self.logger
        self.config.access_log_format = '%(h)s %(l)s %(l)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)s'
        self.app = App(config=app_config, mqtt_topic_signal=mqtt_topic_signal, **kwargs)

    def run(self):
        return serve(
            self.app,
            self.config,
            shutdown_trigger=self.shutdown_event.wait,
        )

    async def stop(self):
        self.logger.info('stopped')
