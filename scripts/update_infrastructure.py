import scrape_lines
import scrape_line
# import redis_save_stops
import redis


def main():
    SELECTED_LINES = ['01N', '02K', '03K']
    stops = get_line_stops(SELECTED_LINES)
    print(stops)


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


if __name__ == "__main__":
    main()
