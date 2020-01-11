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


def connect(database):
    """Creates the connection object to the database and prints basic information to the console.

    Arguments:
        database {string | int} -- The name of the database to connect into.

    Returns:
        Redis object -- the initialized and connected redis object.
    """

    r = redis.Redis(host='localhost', port=6379, db=database)
    # print(r.info())
    return r


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
        r.hset(suid, 'name',     stop.name)
        r.hset(suid, 'md',       params['md'])
        r.hset(suid, 'sn',       params['sn'])
        r.hset(suid, 'start',    params['start'])
        r.hset(suid, 'sorder',   params['sorder'])
        r.hset(suid, 'rc',       params['rc'])
        r.hset(suid, 'line',     params['line'])
        r.hset(suid, 'dir',      params['dir'])

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
        r.hset(luid, 'uid',     line.uid)
        r.hset(luid, 'name',    line.name)
        r.hset(luid, 'number',  line.number)
        r.hset(luid, 'md',      params['md'])
        r.hset(luid, 'sn',      params['sn'])
        r.hset(luid, 'line',    params['line'])  # -> uid

        # 'lines' -> '02K': 250
        r.hset('lines', line.number, line.uid)


def save(stops=None, lines=None):
    r = connect(database=0)
    if lines is not None:
        save_lines(r, lines)
    if stops is not None:
        save_stops(r, stops)

    # r.flushall()
    # print([s.uid for s in stops])
