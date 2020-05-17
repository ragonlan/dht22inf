#!/usr/bin/python3
# -*- coding: utf-8 -*-

import Adafruit_DHT
import socket
from influxdb import InfluxDBClient
from time import sleep
import netifaces as ni
import argparse
import logging
import pprint
import re

FORMAT = '%(asctime)-15s %(name)s [%(process)d] %(levelname)s: %(message)s'

frequency = 8 #seconds. Never should be less than 2 seconds.

sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }

class PrettyLog():
    def __init__(self, obj):
        self.obj = obj

    def __repr__(self):
        return pprint.pformat(self.obj)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Add temperatur and Humidity to influxdb')
    parser.add_argument(
        '-d', '--debug',
        help="Debug mode with no acction.",
        action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.WARNING,
    )
    parser.add_argument('--tag', action='store', default=dict(), nargs='*',
                        required=False, type=str, help='Add this tag to every metric. Syntax tag=value')
    parser.add_argument('--sensor', required=True, choices=sensor_args.keys(), default=None, help='Sensor type: 11, 23 or 2302' )
    parser.add_argument('--pin', required=True, type=int, help='GPIO pin, for example: 4')
    parser.add_argument('--influxdatabase', required=False, type=str, default='temperature', help='Influx Database to store temperature')
    parser.add_argument('--influxserver', required=False, type=str, default='localhost', help='Influx server hostname')
    parser.add_argument('--loop', required=False, action='store_true', default=False, help='Only excetue forever')
    parser.add_argument('--frequency', required=False, type=int, default=frequency, help='Temperature/humidity reading frequency')
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
            extratags[f[0]] = f[1]
    # logging.info(PrettyLog(extratags))
    return extratags

try:
    args = parse_args()
    args.sensor = sensor_args[args.sensor]
    logging.basicConfig(level=args.loglevel, format=FORMAT)
    extratags = parseTags(args.tag)
    ip = 'No IP'
    if ni.ifaddresses('eth0') and ni.AF_INET in ni.ifaddresses('eth0'):
        ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
    elif ni.ifaddresses('wlan0') and ni.AF_INET in ni.ifaddresses('wlan0'):
        ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    if not args.loglevel == logging.DEBUG:
        logging.debug('Debug mode, not storing data to influxdb server.')
        client = InfluxDBClient(host='localhost', database=args.influxdatabase)
    else:
        logging.debug('Debug mode, not storing data to influxdb server.')
    while True:
        humi, temp = Adafruit_DHT.read_retry(args.sensor, args.pin)
        logging.debug(
            'Temp: {:.1f}*C Humity: {:.1f}% IP: {} ExTags: {}'.format(temp, humi, ip, extratags))
        json_body = [
            {
                "measurement": "temp",
                "tags": {
                    "host": socket.gethostname(),
                    "ip": ip,
                },
                "fields": {
                    "temp": temp,
                    "humi": humi
                }
            }
        ]
        json_body[0]['fields'].update(extratags)
        if not args.loglevel == logging.DEBUG:
            client.write_points(json_body)
        if (not args.loop):
            break
        sleep(args.frequency)
except KeyboardInterrupt:
    pass
