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
    print(r.info())
    return r


def create_hash(r, stops):
    """Creates all the required hashes for stop info storage

    Arguments:
        stops {Stop object} -- A list of Stop objects to add to Redis
    """

    for stop in stops:

        uid = 's{}'.format(stop.uid)
        params = stop.params

        r.hset(uid, 'name',     stop.name)
        r.hset(uid, 'md',       params['md'])
        r.hset(uid, 'sn',       params['sn'])
        r.hset(uid, 'start',    params['start'])
        r.hset(uid, 'sorder',   params['sorder'])
        r.hset(uid, 'rc',       params['rc'])
        r.hset(uid, 'line',     params['line'])
        r.hset(uid, 'dir',      params['dir'])


def save(stops):
    r = connect(database=0)
    # r.flushall()
    print([s.uid for s in stops])
    create_hash(r, stops)
