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


# from pprint import pprint
def make_wave(mc, element, centre=(0, 0), steps=20, magnitude=20, duration=5.0):
    wave_shape = sin_wave(steps, magnitude)
    def get_wave_value(i):
        try:
            assert i >= 0
            return wave_shape[i]
        except:
            return 0
    get_wave_map = np.vectorize(get_wave_value)
    prior_condition = mc.get(element)
    distance_map = make_distance_map(prior_condition, centre)
    min_distance = distance_map.min()
    max_distance = distance_map.max()
    total_steps = steps + max_distance - min_distance
    sleep_time = float(duration) / total_steps
    for step in range(total_steps) + min_distance:
        index_map = (step - distance_map + 1) * np.less_equal(distance_map, step) - 1
        increment_map = get_wave_map(index_map)
        new_condition = prior_condition + increment_map
        mc.set(element, new_condition)
        sleep(sleep_time)
        prior_condition = mc.get(element)


def sin_wave(steps=20, magnitude=20):
    steps = (int(steps) / 4 * 4) or 4
    ix = np.arange(steps + 1)
    signal = np.sin(2 * np.pi * ix / steps) * magnitude
    diffs = np.diff(signal)
    return diffs.astype(int)


def make_distance_map(target_array, centre):
    centre = np.array(centre)
    distance_map = np.zeros_like(target_array)
    for i in range(target_array.shape[0]):
        for j in range(target_array.shape[1]):
            distance_map[i, j] = np.linalg.norm(centre - (i, j))

    return distance_map
