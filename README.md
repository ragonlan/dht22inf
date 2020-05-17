# dht22inf
Add metrics to influx from a dht22 sensor in Raspberry Pi

```
usage: dht22inf.py [-h] [-d] [--tag [TAG [TAG ...]]] --sensor {11,22,2302}
                   --pin PIN [--influxdatabase INFLUXDATABASE]
                   [--influxserver INFLUXSERVER] [--loop]
                   [--frequency FREQUENCY]

Add temperatur and Humidity to influxdb

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Debug mode with no acction.
  --tag [TAG [TAG ...]]
                        Add this tag to every metric. Syntax tag=value
  --sensor {11,22,2302}
                        Sensor type: 11, 23 or 2302
  --pin PIN             GPIO pin, for example: 4
  --influxdatabase INFLUXDATABASE
                        Influx Database to store temperature
  --influxserver INFLUXSERVER
                        Influx server hostname
  --loop                Only excetue forever
  --frequency FREQUENCY
                        Temperature/humidity reading frequency
```

Example:
```
./dht22infv2.py  --sensor 2302 --pin 4 -d --tag floor=2  side=east
./dht22inf.py --sensor 2302 --pin 4 --debug  --loop --tag hello=1 mundo=2 --freq 10
```

Output:
```
2018-12-19 15:27:48,587 root [1522] INFO: Temp: 24.8*C Humity: 32.1% IP: 192.4.1.33 ExTags: {'floor': '2', 'side': 'east'}
```
