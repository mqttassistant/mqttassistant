import argparse
import time
from mqttassistant.app import Application


def main():
    parser = argparse.ArgumentParser(prog='mqttassistant', description='MqttAssistant')
    kwargs = vars(parser.parse_args())
    app = Application(**kwargs)
    while True:
        try:
            app.start()
        except KeyboardInterrupt:
            app.stop()
            exit(0)
        # Wait a little before restarting app
        time.sleep(5)
        print('Restarting app')


if __name__ == '__main__':
    main()
