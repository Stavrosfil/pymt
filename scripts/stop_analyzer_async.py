import async_requests
from modules import Stop as Stop
import time
from influxdb import InfluxDBClient
import redis_operations as ro
import redis

'''
A script to analyze a selected stop and output the data to an InfluxDB server.

TODO: Input is a line or a stop?
'''

stop_dirs = {}


def main():

    r = redis.Redis(host='localhost', port=6379, db=0)

    stop_ids = []
    SELECTED_LINES = ['01N', '01X', '02K', '03K']
    # SELECTED_LINES = [l.decode('utf-8') for l in r.hkeys('lines')]
    stop_ids = ro.get_line_stops(SELECTED_LINES)
    print(stop_ids)

    for stop in stop_ids:
        stop_dirs[stop] = int(r.hget('stop{}'.format(stop), 'dir'))

    client = InfluxDBClient('localhost', 8089)
    client.create_database('bus_arrivals')
    client.switch_database('bus_arrivals')
    # print(client.get_list_database())

    loop_timer = time.time()

    while True:

        saveToInflux(client, stop_ids)

        time.sleep(32.0 - ((time.time() - loop_timer) % 32.0))


def saveToInflux(client, stop_ids):

    # stop_ids = stop_ids[0:50]

    print("\n>>> Quering async requests to server...")
    time1 = time.time()
    responses = async_requests.get_stops(stop_ids)
    print("Received {} responses in {} seconds".format(len(responses), time.time() - time1))

    print("\n>>> Writing data to influxdb server...")
    time2 = time.time()

    json_body = []

    for response, stop_id in zip(responses, stop_ids):

        stop = Stop.Stop(response, stop_id)

        if(stop is not None):

            for bus in stop.buses:

                json_body.append(
                    {
                        "measurement": "busArival",
                        "tags": {
                            "bus_id": bus.bus_id,
                            "line_number": bus.line_number,
                            "stop_id": stop_id,
                            "direction": stop_dirs[stop_id]
                        },
                        "time": bus.timestamp,
                        "fields": {
                            "estimated_arival": bus.arival
                        }
                    }
                )

    try:
        client.write_points(json_body)
        # print(json_body)
    except Exception as e:
        print("There was an error writing to the database: {}".format(e))

    print("Files successfully written in {} seconds".format(time.time() - time2))


if __name__ == '__main__':
    main()
