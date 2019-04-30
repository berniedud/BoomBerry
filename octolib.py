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

    cell_range, columns = cell_range
    minrow, maxrow = get_min_max(target_array.shape[0], cell_range)
    mincol, maxcol = get_min_max(target_array.shape[1], columns)
    target_array[minrow: maxrow, mincol: maxcol] = increment


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
    sleep_time, steps = get_sleep_steps(duration, interval, steps)
    increment_map = get_element_shape(mc, element, ranges) * increment

    for _ in range(steps):
        sleep(sleep_time)
        element_array = mc.get(element)
        element_array += increment_map

        set_element(mc, element_array, element)


def get_element_shape(mc, element, ranges=None, cache={}):
    # this caching method is broken!
    element_shape = cache.get(element)
    if element_shape is None:
        element_shape = np.zeros_like(mc.get(element))
        cache[element] = element_shape.copy()
    if ranges is None or ranges == []:
        element_shape += 1
    else:
        for cell_range in ranges:
            set_range(element_shape, cell_range, 1)
    return element_shape


def get_sleep_steps(duration, interval, steps):
    try:
        if not interval:
            sleep_time = float(duration) / steps
        else:
            sleep_time = interval
        if not steps:
            steps = float(duration) / sleep_time
    except:
        raise ValueError('require two of steps, duration or interval, as numbers')
    return sleep_time, steps


def set_element(mc, array_to_set, element):
    max_map, min_map = get_min_max_maps(mc, element)
    array_to_set = np.maximum(array_to_set, min_map)
    array_to_set = np.minimum(array_to_set, max_map)
    mc.set(element, array_to_set)


def get_min_max_maps(mc, element, cache={}):
    cached_value = cache.get(element)
    if not cached_value:
        min_map = np.zeros_like(mc.get(element)) + MIN_THRESHOLD
        max_map = np.zeros_like(min_map) + MAX_THRESHOLD
        cache[element] = (min_map, max_map)
    else:
        min_map, max_map = cached_value
    return max_map, min_map


def flash_element(mc, element, intensity, ranges=None, duration=0.4):
    flash_mask = get_element_shape(mc, element, ranges)
    prior_condition = mc.get(element)

    flash_condition = (1 - flash_mask) * prior_condition + flash_mask * intensity

    set_element(mc, flash_condition, element)
    sleep(duration)
    set_element(mc, prior_condition, element)


from pprint import pprint
def make_wave(mc, element, centre=(0, 0),
              steps=4, magnitude=20, duration=5.0,
              interval=None, iterations=1):

    sleep_time, steps = get_sleep_steps(duration, interval, steps)
    wave_shape = sin_wave(steps, magnitude, iterations)
    element_shape = get_element_shape(mc, element)
    distance_map = make_distance_map(element_shape, centre)
    min_distance = distance_map.min()
    max_distance = distance_map.max()
    total_steps = steps * iterations + max_distance - min_distance

    for step in np.arange(total_steps) + min_distance + 1:
        # increment indices ...
        index_map = (step - distance_map) * np.less_equal(distance_map, step)
        # but only as far as the number of steps
        index_map *= np.less_equal(index_map, wave_shape.size)
        # zeroes become -1, the special index:
        index_map -= 1
        # use lovely numpy indexing to get wave value
        increment_map = wave_shape[index_map]
        # then make new values
        prior_condition = mc.get(element)
        new_condition = prior_condition + increment_map
        mc.set(element, new_condition)
        sleep(sleep_time)


def sin_wave(steps=20, magnitude=20, iterations=1):
    steps = (int(steps) / 4 * 4) or 4
    ix = np.arange(steps * iterations + 2)
    signal = np.sin(2 * np.pi * ix / steps) * magnitude
    diffs = np.diff(signal)
    # special final value for -1 index
    diffs[-1] = 0
    return diffs.astype(int)


def make_distance_map(target_array, centre):
    centre = np.array(centre)
    distance_map = np.zeros_like(target_array)
    for i in range(target_array.shape[0]):
        for j in range(target_array.shape[1]):
            distance_map[i, j] = np.linalg.norm(centre - (i, j))

    return distance_map
