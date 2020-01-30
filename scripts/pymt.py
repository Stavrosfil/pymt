import async_requests
import time
from influxdb import InfluxDBClient
import redis_operations as ro

'''
A script to analyze a selected stop and output the data to an InfluxDB server.

TODO: Input is a line or a stop?
'''

stop_dirs = {}


def main():

    SELECTED_LINES = ['01N', '01X', '02K', '03K', '10', '07', '31']
    # SELECTED_LINES = ro.get_all_lines()[:50]
    stops = ro.get_line_stops(SELECTED_LINES)
    print(stops)

    client = InfluxDBClient('localhost', 8089)
    client.create_database('bus_arrivals')
    client.switch_database('bus_arrivals')

    loop_timer = time.time()

    while True:

        print("\n>>> Quering async requests to server...")
        time1 = time.time()

        try:
            responses = async_requests.get_stops([s.uid for s in stops])
            print("Received {} responses in {} seconds".format(len(responses), time.time() - time1))
        except Exception as e:
            print("There was an exception while getting data from the server: {}".format(e))

        if responses != []:
            for response, stop in zip(responses, stops):
                try:
                    stop.update(response)
                except Exception as e:
                    print("There was an exception while parsing received response: {}".format(e))

        saveToInflux(client, stops)

        time.sleep(32.0 - ((time.time() - loop_timer) % 32.0))


def saveToInflux(client, stops):

    print("\n>>> Writing data to influxdb server...")
    time2 = time.time()

    json_body = []

    for stop in stops:

        if(stop is not None):

            for bus in stop.buses:

                json_body.append(
                    {
                        "measurement": "busArival",
                        "tags": {
                            "bus_id": bus.bus_id,
                            "line_number": bus.line_number,
                            "stop_id": stop.uid,
                            "direction": stop.params['dir']
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
        print("Files successfully written in {} seconds".format(time.time() - time2))
    except Exception as e:
        print("There was an error writing to the database: {}".format(e))


if __name__ == '__main__':
    main()
