FROM python:3.10.1-alpine3.15

# Packages
RUN apk add --no-cache su-exec

# Requirements
COPY requirements.txt /etc/requirements.txt
RUN pip --disable-pip-version-check install -r /etc/requirements.txt

# Docker dir
COPY docker /docker/
RUN mv /docker/mqttassistant /usr/local/bin/

# Source
COPY mqttassistant /usr/local/lib/python3.10/mqttassistant

ENTRYPOINT ["/docker/entrypoint.sh"]
CMD [ "mqttassistant", "--web-port", "80" ]
