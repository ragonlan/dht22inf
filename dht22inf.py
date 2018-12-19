#!/usr/bin/python3
# -*- coding: utf-8 -*-

import Adafruit_DHT as dht
import socket
from influxdb import InfluxDBClient
from time import sleep
import netifaces as ni
import argparse
import logging
import pprint
import re

FORMAT = '%(asctime)-15s %(name)s [%(process)d] %(levelname)s: %(message)s'

class PrettyLog():
    def __init__(self, obj):
        self.obj = obj
    def __repr__(self):
        return pprint.pformat(self.obj)

def parse_args():
    parser = argparse.ArgumentParser(
                    description='Add temperatur and Humidity to influxdb')
    parser.add_argument(
        '-v', '--verbose',
        help="Be verbose",
        action="store_const", dest="loglevel", const=logging.INFO, default=logging.WARNING,
        )
    parser.add_argument( '--tag', action='store', default=dict(), nargs='*', required=False, type=str, help='Add this tag to every metric. Syntax tag=value')
    return parser.parse_args()

def parseTags(tags):
    extratags = dict()
    if not tags:
        return dict()
    for t in tags:
#        logging.info(t)
        if not '=' in t:
            logging.warn('error in tag syntax: {}'.format(t))
            return {}
        else:
            f = t.split('=')
            extratags[f[0]]=f[1]
    return extratags
try:
    args = parse_args()
    logging.basicConfig(level=args.loglevel, format=FORMAT)
    extratags = parseTags(args.tag)
    ip = 'No IP'
    if ni.ifaddresses('eth0') and ni.AF_INET in ni.ifaddresses('eth0'):
      ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
    elif ni.ifaddresses('wlan0') and ni.AF_INET in ni.ifaddresses('wlan0'):
      ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']

    client = InfluxDBClient(host='localhost', database='temperature')
    while 1:
        humi, temp = dht.read_retry(dht.DHT22, 23)
        logging.info('Temp: {:.1f}*C Humity: {:.1f}% IP: {} ExTags: {}'.format(temp, humi, ip, extratags))
        json_body = [
            {
                "measurement": "temp",
                "tags": {
                    "host": "raspberryHome",
                    "ip": ip,
                },
                "fields": {
                    "temp": temp,
                    "humi": humi
                }
            }
        ]
        json_body[0]['fields'].update(extratags)
        client.write_points(json_body)
        sleep(20)

except KeyboardInterrupt:
    pass
