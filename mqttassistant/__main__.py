import argparse
from mqttassistant.app import Application


def main():
    parser = argparse.ArgumentParser(prog='mqttassistant', description='MqttAssistant')
    parser.add_argument('--web-host', default='0.0.0.0')
    parser.add_argument('--web-port', default=8000)
    kwargs = vars(parser.parse_args())
    app = Application(**kwargs)
    app.start()


if __name__ == '__main__':
    main()
