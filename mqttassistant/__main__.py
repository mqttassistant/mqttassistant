import argparse
import os
from pathlib import Path
from mqttassistant.app import Application


WEB_HOST = os.getenv('WEB_HOST', '0.0.0.0')
WEB_PORT = int(os.getenv('WEB_PORT', '8000'))
MQTT_HOST = os.getenv('MQTT_HOST', '127.0.0.1')
MQTT_PORT = int(os.getenv('MQTT_PORT', '1883'))
MQTT_USERNAME = os.getenv('MQTT_USERNAME', '')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD', '')
MQTT_NAME = os.getenv('MQTT_NAME', 'mqttassistant')
MQTT_KEEP_ALIVE = int(os.getenv('MQTT_KEEP_ALIVE', '5'))
MQTT_DISCOVERY_TOPIC = os.getenv('MQTT_DISCOVERY_TOPIC', 'homeassistant')
UI_PATH = os.getenv('UI_PATH', Path(__file__).parent.parent / 'ui' / 'build' / 'web')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')


def main():
    parser = argparse.ArgumentParser(prog='mqttassistant', description='MqttAssistant')
    parser.add_argument('--config-path', type=Path, default=Path.cwd())
    parser.add_argument('--web-port', default=WEB_PORT)
    parser.add_argument('--mqtt-host', default=MQTT_HOST)
    parser.add_argument('--mqtt-port', default=MQTT_PORT)
    parser.add_argument('--mqtt-username', default=MQTT_USERNAME)
    parser.add_argument('--mqtt-password', default=MQTT_PASSWORD)
    parser.add_argument('--mqtt-name', default=MQTT_NAME)
    parser.add_argument('--mqtt-keep-alive', default=MQTT_KEEP_ALIVE)
    parser.add_argument('--mqtt-discovery-topic', default=MQTT_DISCOVERY_TOPIC)
    parser.add_argument('--ui-path', default=UI_PATH)
    parser.add_argument('--log-level', default=LOG_LEVEL)
    kwargs = vars(parser.parse_args())
    app = Application(**kwargs)
    app.start()


if __name__ == '__main__':
    main()
