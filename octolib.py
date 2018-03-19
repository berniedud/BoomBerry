import numpy as np
import memcache
from time import sleep

red = green = blue = locks = np.zeros([8,8], int)
octo_grid_zeros = dict(
    red=red,
    green=green,
    blue=blue,
    locks=locks
)

mc = memcache.Client(['127.0.0.1:11211'])
MIN_THRESHOLD = 0
MAX_THRESHOLD = 255


def reset_zeroes(mc):
    mc.set_multi(octo_grid_zeros)


def set_range(target_array, cell_range, increment):
    def get_min_max(axis_size, cell_range):
        if cell_range is None:
            min = 0
            max = axis_size
        elif isinstance(cell_range, tuple):
            min = cell_range[0]
            max = cell_range[1] + 1
        else:
            min = cell_range
            max = cell_range + 1
        return min, max

        return 1, 2
    cell_range, columns = cell_range
    minrow, maxrow = get_min_max(target_array.shape[0], cell_range)
    mincol, maxcol = get_min_max(target_array.shape[1], columns)
    target_array[minrow: maxrow, mincol: maxcol] += increment


def ramp_colour(mc, element, ranges=None, increment=1, steps=1, duration=2, interval=None):
    '''

    :param mc: memcache object
    :param element: name of element to change in memcache object
    :param ranges: list of ranges to change. Each range to take to be a tuple:
            (2, 4)              row 2, column 4
            (1, None)           all of row 1
            ((2, 5), (6, 7))    cells in rows 2 to 5 AND columns 6 to 7
    :param increment: amount to change per step
    :param steps: number of steps to take
    :param duration: total duration
    :param interval: time between steps
    :return:
    '''
    try:
        if not interval:
            sleep_time = float(duration) / steps
        else:
            sleep_time = interval
        if not steps:
            steps = float(duration) / sleep_time
    except:
        raise
        # raise ValueError('require two of steps, duration or interval, as numbers')

    increment_map = np.zeros_like(mc.get(element))
    if ranges is None or ranges == []:
        increment_map += increment
    else:
        for cell_range in ranges:
            set_range(increment_map, cell_range, increment)

    max_map, min_map = get_min_max_maps(mc, element)


    for _ in range(steps):
        sleep(sleep_time)
        element_array = mc.get(element)
        element_array += increment_map

        set_element(mc, element_array, element, min_map, max_map)


def set_element(mc, array_to_set, element, min_map, max_map):
    array_to_set = np.maximum(array_to_set, min_map)
    array_to_set = np.minimum(array_to_set, max_map)
    mc.set(element, array_to_set)


def get_min_max_maps(mc, element):
    min_map = np.zeros_like(mc.get(element))
    min_map += MIN_THRESHOLD
    max_map = np.zeros_like(mc.get(element))
    max_map += MAX_THRESHOLD
    return max_map, min_map


def flash_element(mc, element, value, duration=0.4):
    max_map, min_map = get_min_max_maps(mc, element)
    prior_condition = mc.get(element)
    flash_condition = np.zeros_like(prior_condition)
    flash_condition += value

    set_element(mc, flash_condition, element, min_map, max_map)
    sleep(duration)
    set_element(mc, prior_condition, element, min_map, max_map)
