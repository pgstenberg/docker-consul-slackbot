#!/bin/bash

/bin/consul watch -http-addr=$CONSUL_ADDRESS -type=$CONSUL_WATCH_TYPE $CONSUL_OPTIONS /bin/consul-slackbot.py
