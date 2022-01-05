import os
import sys
import logging
from datetime import datetime

from logging.handlers import TimedRotatingFileHandler

from miio.airpurifier_miot import AirPurifierMiot, AirPurifierMiotStatus
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
stdout_handler.setFormatter(formatter)

file_handler = TimedRotatingFileHandler('logs/logs.log',
                                        when='D',
                                        interval=1,
                                        backupCount=30)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)

def uncaught_handler(type, value, tb):
    logger.exception("Uncaught exception: {0}".format(str(value)))

sys.excepthook = uncaught_handler


token = os.environ.get('INFLUX_TOKEN')
org = "victor.penelski@gmail.com"
bucket = "victor.penelski's Bucket"
influx_url = "https://eu-central-1-1.aws.cloud2.influxdata.com"

apm = AirPurifierMiot(os.environ.get('XIAOMI_URL'), os.environ.get('XIAOMI_TOKEN'))
print(apm)
print(os.environ.get('XIAOMI_URL'))
status: AirPurifierMiotStatus = apm.status()
logger.info(status)

with InfluxDBClient(url=influx_url, token=token, org=org) as client:
    now = datetime.utcnow()
    point = Point("mem"  # fluent interfaces are so ugly in python :O
                    ).tag("host", "zaichar1"
                    ).field("filter_hours_used", status.filter_hours_used
                    ).field("filter_life_remaining", status.filter_life_remaining
                    ).field("temperature", status.temperature
                    ).field("humidity", status.humidity
                    ).field("is_on", status.is_on
                    ).field("use_time", status.use_time
                    ).field("aqi", status.aqi
                    ).time(now, WritePrecision.NS)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket, org, point)
    logger.info(f'successfully wrote to InfluxDB bucket: {bucket} at utcnow: {now}')
