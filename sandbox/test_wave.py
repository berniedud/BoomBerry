from octolib import mc, ramp_colour, reset_zeroes, make_wave

reset_zeroes(mc)

make_wave(mc, 'blue', centre=(0,0), duration=10, steps=20, magnitude=100)
