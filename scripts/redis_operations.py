import scrape_lines
import scrape_line
import redis


"""
A script to communicate with the local Redis database server.

The purpose of the database it creates is to cache and store all the data about the stop network of the buses.
Every required info to create the request url for the particular stop is stored in here.

The architecture makes use of Redis hashes for really fast performance and better structure.


- Example 1, a url to get the telematics about a stop:

http://m.oasth.gr/#index.php?md=4&sn=3&start=819&sorder=1&rc=2282&line=620&dir=1


- Example 2, a better, json-like structured stop object, as it should be stored in Redis:

stop_example = {
    'id': 819,
    'name': 'testerino',
    'lines': [
        {'02K': 3},
        {'01N': 1},
    ],
    'direction': 1,
    'sn': 3,
    'md': 4,
    'sorder': 3,
    'rc': 2,
    'line': 2
}
"""


# def main():
#     SELECTED_LINES = ['01N', '02K', '03K']
#     stops = get_line_stops(SELECTED_LINES)
#     print(stops)


def connect(database=0):
    """Creates the connection object to the database and prints basic information to the console.

    Arguments:
        database {string | int} -- The name of the database to connect into.

    Returns:
        Redis object -- the initialized and connected redis object.
    """

    r = redis.Redis(host='localhost', port=6379, db=database)
    return r

# ---------------------------------------------------------------------------- #
#                                    SAVING                                    #
# ---------------------------------------------------------------------------- #


def save_stops(r, stops):
    """Creates all the required hashes for stop info storage

    Arguments:
        stops {Stop object} -- A list of Stop objects to add to Redis
    """

    for stop in stops:

        # e.g 's819': Stop 819
        suid = 'stop{}'.format(stop.uid)
        params = stop.params

        # Add parameters to the s prefixed hash.
        stop_attributes = {'name': stop.name}
        stop_attributes.update(params)

        r.hmset(suid, stop_attributes)

        # e.g. 'l819': Lines for stop 819
        luid = 'stop{}:lines'.format(stop.uid)

        # Add available lines to the 'l' prefixed hash.
        r.hset(luid, str(params['line']), params['sorder'])

        lsuid = 'line{}:stops:direction{}'.format(
            params['line'], params['dir'])

        r.hset(lsuid, stop.uid, params['sorder'])


def save_lines(r, lines):

    for line in lines:

        # e.g. 'l02k': Line O2K
        luid = 'line{}'.format(line.uid)
        params = line.params

        # Add parameters to the hash
        line_attributes = {
            'uid':     line.uid,
            'name':    line.name,
            'number':  line.number,
        }
        line_attributes.update(params)
        r.hmset(luid, line_attributes)

        # 'lines' -> '02K': 250
        r.hset('lines', line.number, line.uid)


def save(stops=None, lines=None):
    r = connect(database=0)
    if lines is not None:
        save_lines(r, lines)
    if stops is not None:
        save_stops(r, stops)


# ---------------------------------------------------------------------------- #
#                                    LOADING                                   #
# ---------------------------------------------------------------------------- #


def get_line_stops(selected_lines, db=0):

    selected_stops = set()

    # Initialize Redis client object
    r = redis.Redis(host='localhost', port=6379, db=db)

    # Load lines from Redis cache into dictionary
    selected_lines_uids = set([int(l) for l in r.hmget('lines', selected_lines)])
    # print(selected_lines_uids)

    for line_uid in selected_lines_uids:
        for direction in (1, 2):
            lsuid = 'line{}:stops:direction{}'.format(line_uid, direction)
            stops = [int(s) for s in r.hgetall(lsuid).keys()]
            selected_stops.update(stops)

    return selected_stops


# ---------------------------------------------------------------------------- #
#                             UPDATE INFRASTRUCTURE                            #
# ---------------------------------------------------------------------------- #


def redis_update_infrastructure(db=0):

    # Initialize Redis client object
    r = redis.Redis(host='localhost', port=6379, db=db)

    # Clean all lines in db
    r.flushdb()

    # Scrape all indivudual lines and save them
    # TODO: Do not use saving by default inside scrape_lines
    scrape_lines.scrape_lines()

    # Load all line UIDs in memory
    lines = [l.decode('utf-8') for l in r.hvals('lines')]

    # Use line UID to scrape individual lines
    for line in lines:
        scrape_line.scrape_line(line)

    # Save database to memory
    r.save()


# if __name__ == "__main__":
#     main()
