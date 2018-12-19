# dht22inf
Add metrics to influx from a dht sensor
```
usage: dht22infv2.py [-h] [-v] [--tag [TAG [TAG ...]]]

Add temperatur and Humidity to influxdb

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Be verbose
  --tag [TAG [TAG ...]]
                        Add this tag to every metric. Syntax tag=value
```

Example:
```
./dht22infv2.py -v --tag floor=2  side=east
```

Output:
```
2018-12-19 15:27:48,587 root [1522] INFO: Temp: 24.8*C Humity: 32.1% IP: 192.4.1.33 ExTags: {'floor': '2', 'side': 'east'}
```
