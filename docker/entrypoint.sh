#!/bin/sh
set -e

if [ "$1" = 'mqttassistant' ]; then
    exec su-exec nobody "$@"
else
    exec "$@"
fi
