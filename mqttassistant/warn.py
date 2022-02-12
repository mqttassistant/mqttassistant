import logging
import warnings

IGNORE_WARNINGS_MODULES = [
    'amqtt.client',  # https://github.com/Yakifo/amqtt/issues/96
]
IGNORE_WARNINGS_MESSAGES = [
]


def configure_warnings():
    logging.captureWarnings(True)
    for module in IGNORE_WARNINGS_MODULES:
        warnings.filterwarnings('always', module=module)
    for message in IGNORE_WARNINGS_MESSAGES:
        warnings.filterwarnings('always', message=message)
