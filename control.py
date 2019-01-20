from flask import Flask, jsonify, make_response
from threading import Thread

from octolib import mc, reset_zeroes, ramp_colour

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/octopi/api/v1.0/status', methods=['GET'])
def get_status():
    '''Not needed for anything but a nice test'''
    return jsonify({'status':'OK'})


@app.route('/octopi/api/v1.0/leds/clear', methods=['PUT'])
def put_clear():
    reset_zeroes(mc)
    return jsonify({'status': 'DONE'})


@app.route('/octopi/api/v1.0/leds/ramp/<colour>/<int:increment>/<int:steps>/<int:duration>', methods=['PUT'])
def ramp(colour, ranges=None, increment=1, steps=1, duration=2):
    args = (mc, colour)
    kwargs = dict(increment=increment, steps=steps, duration=duration)
    print(kwargs)
    ramp_colour(*args, **kwargs)
    return jsonify({'status': 'RAMPING'})


@app.route('/octopi/api/v1.0/leds', methods=['GET'])


@app.route('/octopi/api/v1.0/leds', methods=['GET'])
@app.route('/octopi/api/v1.0/leds/<colour>', methods=['GET'])
def get_leds(colour=None):
    print('got colour: {}'.format(colour))
    if colour:
        colours = make_list(colour)
    else:
        colours=['red', 'green', 'blue']
    print('colours: {}'.format(colours))
    leds = {}
    for c in colours:
        print
        leds[c] = [list(row) for row in mc.get(c)]
    return jsonify(leds)


def make_list(thing):
    if not thing:
        return list(None)
    elif isinstance(thing, list):
        return thing
    else:
        return [thing]

if __name__ == '__main__':
    app.run(debug=True)
