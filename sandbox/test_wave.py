from octolib import mc, reset_zeroes, make_wave

#reset_zeroes(mc)

while True:
    make_wave(mc, 'blue', centre=(0,0), duration=4, steps=60, magnitude=100, iterations=3)
    make_wave(mc, 'red', centre=(0,7), duration=4, steps=60, magnitude=100, iterations=3)
    make_wave(mc, 'green', centre=(7,7), duration=4, steps=60, magnitude=100, iterations=3)

