import folium
from pymt import config, default_logger


class Conf(object):
    def __init__(self, d):
        self.__dict__ = d


c = Conf(config['map'])


@default_logger.timer()
def init_map():
    m = folium.Map(location=c.initial_location, tiles=c.map_styles[c.default_style],
                   zoom_start=c.initial_zoom)
    for option in c.map_styles:
        folium.TileLayer(option).add_to(m)

    # other mapping code (e.g. lines, markers etc.)
    folium.LayerControl().add_to(m)
    return m


def save_map(m):
    m.save("map.html")


def simple_plot(m, coords: list):
    for coord in coords:
        folium.Circle(
            radius=50,
            location=coord,
            fill_color='#3186cc',
            color='clear',
            fill=True,
            fill_opacity=1,
        ).add_to(m)


def plot_bus(m, bus):
    coords = (bus.lat, bus.lon)
    folium.Circle(
        radius=100,
        location=coords,
        # popup=bus.route_code,
        tooltip=bus.uuid,
        fill_color='red',
        color='clear',
        fill=True,
        fill_opacity=.75,
    ).add_to(m)


def plot_route(m, line, days=None, draw_points=c.draw_points, draw_lines=c.draw_lines):
    if days is None:
        days = [0, 1]
    if line:
        coords = []
        for day in days:
            for stop in line.stops[day]:
                if stop:
                    coord = (stop.lat, stop.lon)
                    coords.append(coord)
                    if draw_points:
                        folium.Circle(
                            radius=50,
                            location=coord,
                            popup=stop.desc_el,
                            tooltip=stop.desc_el,
                            fill_color='#3186cc',
                            color='clear',
                            fill=True,
                            fill_opacity=1,
                        ).add_to(m)
        if draw_lines and coords:
            folium.PolyLine(coords, color="black", weight=2, opacity=0.3).add_to(m)

# folium.Marker(
#     location=coord,
#     popup=stop['desc_el'],
#     tooltip=stop['desc_el'],
# ).add_to(m)

# folium.CircleMarker(
#     location=[stop['lat'], stop['lon']],
#     radius=50,
#     popup='Test',
#     color='#3186cc',
#     fill=True,
#     fill_color='#3186cc'
# ).add_to(m)
