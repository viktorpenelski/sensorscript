A script for gathering sensor data from Mi Air Purifier 3H and publishing it to Influx DB

The following environment variables are mandatory:

| variable       | example value      | description                                                                        |
| -------------- | ------------------ | ---------------------------------------------------------------------------------- |
| `INFLUX_TOKEN` | AZ32h-Fw2ah3d4w... | API key for the destination InfluxDB installation                                  |
| `XIAOMI_TOKEN` | 2g9z35g4gh4232h... | Token for local network access to the Mi Air Purifier                              |
| `XIAOMI_URL`   | 192.168.1.101      | Network address where Mi Air Purifier is reachable. Don't forget to make it static |

they can be included in a `.env` file if the script is ran through `run.sh`