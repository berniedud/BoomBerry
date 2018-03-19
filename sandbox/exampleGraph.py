# example taken from:
# http://jakevdp.github.io/blog/2012/12/06/minesweeper-in-matplotlib/

import numpy as np
import matplotlib.pyplot as pyplot
from time import sleep

from pprint import pprint

click_xy = None

COLOUR_INCREMENT = 0.1
DELAY_SECONDS = 0.05

xy_scale = (8, 8)
graph_image = pyplot.figure()
grid = graph_image.add_subplot(111, xlim=(-1, xy_scale[0] + 1), ylim=(-1, xy_scale[1] + 1))

points = [(x,y) for y in range(xy_scale[1]) for x in range(xy_scale[0])]



# Function to be called when mouse is clicked
def on_click(event):
    found = False
    for x in range(xy_scale[0]):
        for y in range(xy_scale[1]):
            polygon = polygons[(x,y)]['polygon']
            if polygon.contains_point((event.x, event.y)):
                found = True
                global click_xy
                click_xy = (x, y)
                break
        if found:
            break


def on_keypress(event):
    key_map = dict(
        q=bye,
        Q=bye,
        I=invert_colour_all,
        i=invert_colour_point,
        b=add_blue,
        B=subtract_blue,
        r=add_red,
        R=subtract_red,
        g=add_green,
        G=subtract_green,
        P=reset_colour,
        t=fade_red
    )
    key = event.key
    # pprint(key)
    try:
        key_map[key]()
    except KeyError:
        pprint('Key not mapped: {}'.format(key))
        raise


def make_square(point):
    x, y = point
    square = [
        [x      , y     ],
        [x + 1  , y     ],
        [x + 1  , y + 1 ],
        [x      , y + 1 ],
        [x      , y     ],
    ]
    return square


def get_starting_colour(point):
    x, y = point
    red = (x + 1) / 8
    green = (y + 1) / 8
    blue = (x + y + 2) / 16
    return (red, green, blue)


def make_polygons(grid, points):
    polygons = {}
    for point in points:
        polygons[point] = dict(
            polygon=pyplot.Polygon(make_square(point)),
            colour=get_starting_colour(point)
        )
        grid.add_patch(polygons[point]['polygon'])
        polygons[point]['polygon'].set_facecolor(polygons[point]['colour'])
    return polygons


def set_polygon_colour_all():
    for point in polygons.keys():
        polygons[point]['polygon'].set_facecolor(polygons[point]['colour'])


def invert_colour(colour):
    colour = tuple([
        1 - element for element in colour
    ])
    return colour


def invert_colour_all():
    for detail in polygons.values():
        detail['colour'] = invert_colour(detail['colour'])
    set_polygon_colour_all()
    graph_image.canvas.draw()


def invert_colour_point():
    if click_xy:
        polygons[click_xy]['colour'] = invert_colour(polygons[click_xy]['colour'])
        set_polygon_colour_all()
        graph_image.canvas.draw()
    else:
        pprint('No point chosen yet')


def change_all_colour(element, how):
    if click_xy:
        points_to_change = [click_xy]
    else:
        points_to_change = points

    for point in points_to_change:
        # pprint('changing point: {}'.format(point))
        # pprint('was {}'.format(polygons[point]['colour']))
        polygons[point]['colour'] = change_colour(polygons[point]['colour'], element, how)
        # pprint('now {}'.format(polygons[point]['colour']))

    set_polygon_colour_all()
    graph_image.canvas.draw()


def change_colour(original_colour, element, how):
    elements = list(original_colour)
    indices = dict(red=0, green=1, blue=2)
    element_to_change = elements[indices[element]]
    if how == 'add':
        elements[indices[element]] = min(1, element_to_change + COLOUR_INCREMENT)
    elif how == 'subtract':
        elements[indices[element]] = max(0, element_to_change - COLOUR_INCREMENT)
    else:
        pprint('{} not supported'.format(how))
    return tuple(elements)


def reset_colour():
    for point in points:
        polygons[point]['colour'] = get_starting_colour(point)
    graph_image.canvas.draw()


def add_blue():
    change_all_colour('blue', 'add')


def subtract_blue():
    change_all_colour('blue', 'subtract')


def add_red():
    change_all_colour('red', 'add')


def subtract_red():
    change_all_colour('red', 'subtract')


def add_green():
    change_all_colour('green', 'add')


def subtract_green():
    change_all_colour('green', 'subtract')


def fade_red():
    for step in range(int(1 / COLOUR_INCREMENT) + 1):
        change_all_colour('red', 'add')
        change_all_colour('green', 'subtract')
        change_all_colour('blue', 'subtract')
        sleep(DELAY_SECONDS)


def bye():
    pyplot.close()
    exit()



polygons = make_polygons(grid, points)



# Connect the click function to the button press event
graph_image.canvas.mpl_connect('button_press_event', on_click)
graph_image.canvas.mpl_connect('key_press_event', on_keypress)

pyplot.show()
