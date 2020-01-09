import scrape_lines
import scrape_line
import redis_save_stops
import redis


r = redis.Redis(host='localhost', port=6379, db=0)


# UPDATE LINES
def update():
    r.flushall()
    scrape_lines.scrape_lines()
    lines = [l.decode('utf-8') for l in r.hvals('lines')]
    for line in lines:
        scrape_line.scrape_line(line)


# update()


# lines = [int(l) for l in r.hvals('lines')]
lines = {}
for i, j in zip(r.hkeys('lines'), r.hvals('lines')):
    lines[i.decode('utf-8')] = int(j)

# lines = r.lrange('lines', 0, -1)
print(list(lines.keys()))
# print(list(lines.values()))


selected_lines = ['01N', '02K', '03K']
selected_stops = []
for line in selected_lines:
    # print(lines[line])
    for direction in (1, 2):
        lsuid = 'line{}:direction{}:stops'.format(lines[line], direction)
        stops = [int(s) for s in r.hgetall(lsuid).keys()]
        print(stops)
        selected_stops.extend(stops)


r.save()

# print(r.hgetall('s819')[b'name'])
# print(r.hgetall('ls102K'))

print(selected_stops)
