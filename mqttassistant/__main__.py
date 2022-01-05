import argparse
from mqttassistant.app import Application


def main():
    parser = argparse.ArgumentParser(prog='mqttassistant', description='MqttAssistant')
    kwargs = vars(parser.parse_args())
    app = Application(**kwargs)
    app.start()


if __name__ == '__main__':
    main()
