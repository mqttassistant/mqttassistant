FROM python:3.10.1-alpine3.15


COPY docker/mqttassistant /usr/local/bin/
COPY mqttassistant /usr/local/lib/python3.10/site-packages/mqttassistant

CMD [ "mqttassistant" ]