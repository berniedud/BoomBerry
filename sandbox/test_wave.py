from octolib import mc, reset_zeroes, make_wave

reset_zeroes(mc)

make_wave(mc, 'blue', centre=(0,0), duration=4, steps=40, magnitude=100, iterations=2)

