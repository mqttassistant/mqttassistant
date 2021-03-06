import asyncio
import re
from typing import Optional
from amqtt import client
from .dispatch import Signal
from .log import get_logger


class MQTTClient(client.MQTTClient):
    pass
    def __init__(self, *args, on_connect=None, **kwargs):
        self.on_connect = on_connect
        super().__init__(*args, **kwargs)

    async def _do_connect(self):
        await super()._do_connect()
        if self.on_connect:
            await self.on_connect()


class Mqtt:
    def __init__(self, topic_signal: Optional[Signal] = Signal(), **config):
        self.topic_signal = topic_signal
        # Config
        self.logger = get_logger('Mqtt', level=config.get('log_level', 'INFO'))
        self.name = config.get('mqtt_name', 'mqttassistant')
        self.host = config.get('mqtt_host', 'localhost')
        self.port = config.get('mqtt_port', 1883)
        self.username = config.get('mqtt_username', '')
        self.password = config.get('mqtt_password', '')
        self.keep_alive = config.get('mqtt_keep_alive', 5)
        self.discovery_topic = config.get('mqtt_discovery_topic', 'homeassistant')
        self.client_id = self.name
        self.last_will_topic = '{}/state'.format(self.name)
        self.client = self.get_client()
        self.connect_parameters = self.get_connect_parameters()
        # Discovery
        self.discovery_topic_re = re.compile(r'^{}/(?P<component>\w+)/(?:(?P<node_id>[a-zA-Z0-9_-]+)/)?(?P<object_id>[a-zA-Z0-9_-]+)/config$'.format(self.discovery_topic))
        self.discovery_message = dict()
        self.reload_scheduled = False
        # Subcribed topics
        self.subscribed_topics = set()
        self.topic_signal.connect_callback = self.topic_subscribe
        self.topic_signal.disconnect_callback = self.topic_unsubscribe

    def get_client(self):
        return MQTTClient(
            client_id=self.client_id,
            config=self.get_client_config(),
            on_connect=self.on_connect,
        )

    def get_client_config(self):
        return dict(
            keep_alive=self.keep_alive,
            ping_delay=1,
            default_qos=2,
            default_retain=False,
            auto_reconnect=True,
            reconnect_max_interval=5,
            reconnect_retries=-1,
            will=dict(
                retain=True,
                topic=self.last_will_topic,
                message=b'offline',
                qos=1,
            )
        )

    def get_connect_parameters(self):
        auth = ''
        if self.username:
            auth = '{}:{}@'.format(self.username, self.password)
        return dict(
            uri='mqtt://{}{}:{}/'.format(auth, self.host, self.port),
        )

    async def run(self):
        self.logger.info('Started. Server: {}'.format(self.host))
        return await self.connect()

    async def stop(self, **kwargs):
        if self.client.session.transitions.is_connected():
            await self.client.publish(self.last_will_topic, b'offline')
            await self.client.disconnect()
        self.logger.info('Stopped')

    async def connect(self):
        await self.client.connect(**self.connect_parameters)
        asyncio.create_task(self.read_messages())

    async def on_connect(self):
        await self.client.publish(self.last_will_topic, b'online')
        # Subscribe
        discovery_topic = '{}/#'.format(self.discovery_topic)
        await self.client.subscribe([(discovery_topic, 2)])
        self.logger.info('Connected')
        # Subscribed topics
        for topic in self.subscribed_topics:
            await self.client.subscribe([(topic, 2)])

    def _on_message(self, topic, payload, retained):
        asyncio.create_task(self.on_message(topic, payload, retained))

    async def read_messages(self):
        while True:
            try:
                message = await self.client.deliver_message()
                if message:
                    packet = message.publish_packet
                    topic = packet.variable_header.topic_name
                    payload = packet.payload.data.decode('utf-8')
                    await self.on_message(topic, payload)
            except Exception as error:
                self.logger.exception('read_messages', error)

    async def on_message(self, topic, payload):
        self.logger.debug('message received: {} {}'.format(topic, payload))
        # Discovery topic
        match = self.discovery_topic_re.match(topic)
        if match:
            await self.on_discovery_message(topic, payload)
        if topic in self.subscribed_topics:
            await self.topic_signal.send(topic, payload=payload)

    async def on_discovery_message(self, topic, payload):
        if payload:
            if not payload == self.discovery_message.get(topic, None):
                self.discovery_message[topic] = payload
                await self.schedule_reload()
        else:
            if topic in self.discovery_message:
                del self.discovery_message[topic]
                await self.schedule_reload()

    async def schedule_reload(self):
        if not self.reload_scheduled:
            self.reload_scheduled = True
            loop = asyncio.get_event_loop()
            loop.call_later(0.2, self.reload_config)

    def reload_config(self):
        self.reload_scheduled = False
        self.logger.info('Configuration reloaded')

    async def topic_subscribe(self, **kwargs):
        topic = kwargs['subject']
        self.logger.debug('topic_subscribe: {}'.format(topic))
        if not topic in self.subscribed_topics:
            self.subscribed_topics.add(topic)
            if self.client._connected_state.is_set():
                asyncio.create_task(self.client.subscribe([(topic, 2)]))

    async def topic_unsubscribe(self, **kwargs):
        topic = kwargs['subject']
        self.logger.debug('topic_unsubscribe: {}'.format(topic))
        if topic in self.subscribed_topics:
            self.subscribed_topics.remove(topic)
            if self.client._connected_state.is_set():
                asyncio.create_task(self.client.unsubscribe([(topic, 2)]))
